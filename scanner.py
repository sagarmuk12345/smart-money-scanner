import os
import requests
import yfinance as yf

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


def send_discord(message):
    requests.post(
        WEBHOOK_URL,
        json={"content": message}
    )


for ticker in WATCHLIST:

    try:

        df = yf.download(
            ticker,
            period="1y",
            progress=False,
            auto_adjust=True
        )

        print(f"Checked {ticker}")

    except Exception as e:

        print(f"{ticker}: {e}")

send_discord("Scanner is working!")
