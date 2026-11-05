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

    print("Discord Status:", response.status_code)


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
        ma50
