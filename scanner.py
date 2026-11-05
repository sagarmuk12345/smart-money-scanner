import os
import requests
import yfinance as yf
import pandas as pd

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

WATCHLIST = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "NVDA",
    "TSLA",
    "AMD",
    "PLTR",
    "NFLX"
]


def calculate_rsi(close, period=14):
    delta = close.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def send_discord(message):
    response = requests.post(
        WEBHOOK_URL,
        json={"content": message}
    )

    print(f"Discord Status: {response.status_code}")


def scan_stock(ticker):

    try:
        df = yf.download(
            ticker,
            period="2y",
            interval="1d",
            progress=False,
            auto_adjust=True
        )

        if len(df) < 220:
            print(f"{ticker}: Not enough data")
            return

        df["MA50"] = df["Close"].rolling(50).mean()
        df["MA200"] = df["Close"].rolling(200).mean()
        df["RSI"] = calculate_rsi(df["Close"])

        close = float(df["Close"].iloc[-1])
        ma50 = float(df["MA50"].iloc[-1])
        ma200 = float(df["MA200"].iloc[-1])

        rsi_today = float(df["RSI"].iloc[-1])
        rsi_yesterday = float(df["RSI"].iloc[-2])

        trend_ok = (
            close > ma200 and
            ma50 > ma200
        )

        rsi_signal = (
            40 <= rsi_today <= 45 and
            rsi_today > rsi_yesterday
        )

        print(
            f"{ticker} | "
            f"Close={close:.2f} | "
            f"MA50={ma50:.2f} | "
            f"MA200={ma200:.2f} | "
            f"RSI={rsi_today:.2f} | "
            f"Trend={trend_ok} | "
            f"RSI_Signal={rsi_signal}"
        )

        if trend_ok and rsi_signal:

            message = (
  
