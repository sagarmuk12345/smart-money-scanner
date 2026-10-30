import os
import requests
import warnings
warnings.filterwarnings("ignore")

import yfinance as yf

WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

watchlist = [
    "META",
    "GOOGL",
    "AMZN",
    "NVDA",
    "MSFT",
    "AAPL",
    "AMD",
    "TSLA",
    "PLTR"
]

alerts = []

for symbol in watchlist:

    try:

        stock = yf.Ticker(symbol)

        hist = stock.history(period="1mo")

        avg_volume = hist["Volume"].tail(20).mean()
        latest_volume = hist["Volume"].iloc[-1]

        rvol = latest_volume / avg_volume

        if rvol > 2:

          price = hist["Close"].iloc[-1]

alerts.append(
    f"🚀 {symbol}\nPrice = ${price:.2f}\nRVOL = {rvol:.2f}"
)
    except Exception as e:

        print(symbol, e)

if alerts:

    requests.post(
        WEBHOOK,
        json={
            "content": "\n\n".join(alerts)
        }
    )

    print("ALERT SENT")

else:

    print("NO SIGNALS")
