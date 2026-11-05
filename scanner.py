import os
import tempfile
import requests
import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf

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

    rsi = 100 - (100 / (1 + rs))

    return rsi


def generate_chart(df, ticker):

    chart_file = f"{ticker}.png"

    apds = [
        mpf.make_addplot(df["MA50"], color="blue"),
        mpf.make_addplot(df["MA200"], color="red")
    ]

    mpf.plot(
        df,
        type="candle",
        style="yahoo",
        addplot=apds,
        volume=True,
        figsize=(12, 8),
        title=f"{ticker} RSI Pullback Setup",
        savefig=chart_file
    )

    return chart_file


def send_discord(message, image_path):

    with open(image_path, "rb") as f:

        requests.post(
            WEBHOOK_URL,
            data={"content": message},
            files={"file": f}
        )


def scan_stock(ticker):

    try:

        df = yf.download(
            ticker,
            period="2y",
            interval="1d",
            progress=False
        )

        if len(df) < 220:
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
            30 <= rsi_today <= 35 and
            rsi_today > rsi_yesterday
        )

        if trend_ok and rsi_signal:

            chart = generate_chart(df, ticker)

            msg = (
                f"🚀 {ticker}\n\n"
                f"Price: ${close:.2f}\n"
                f"RSI: {rsi_today:.2f} ↑\n"
                f"50MA: {ma50:.2f}\n"
                f"200MA: {ma200:.2f}\n\n"
                f"✅ Price > 200MA\n"
                f"✅ 50MA > 200MA\n"
                f"✅ RSI Turning Up"
            )

            send_discord(msg, chart)

            os.remove(chart)

    except Exception as e:
        print(f"{ticker}: {e}")


def main():

    print("Running scanner...")

    for ticker in WATCHLIST:
        scan_stock(ticker)

    print("Finished")


if __name__ == "__main__":
    main()
