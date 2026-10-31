import os
import requests
import warnings

warnings.filterwarnings("ignore")

import yfinance as yf

try:

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

            if hist.empty:
                continue

            avg_volume = hist["Volume"].tail(20).mean()
            latest_volume = hist["Volume"].iloc[-1]

            rvol = latest_volume / avg_volume

            close_prices = hist["Close"].dropna()

if len(close_prices) < 20:
    continue

price = close_prices.iloc[-1]

            ema20 = hist["Close"].ewm(span=20).mean().iloc[-1]
            ema50 = hist["Close"].ewm(span=50).mean().iloc[-1]

            month_return = (
                (price / hist["Close"].iloc[0]) - 1
            ) * 100

            month_high = hist["High"].max()

            score = 0

            # RVOL
            if rvol > 3:
                score += 20
            elif rvol > 2:
                score += 15
            elif rvol > 1.5:
                score += 10

            # Above 20 EMA
            if price > ema20:
                score += 20

            # Above 50 EMA
            if price > ema50:
                score += 20

            # Momentum
            if month_return > 10:
                score += 20
            elif month_return > 5:
                score += 10

            # Near monthly high
            if price >= month_high * 0.98:
                score += 20

            print(
    f"{symbol} | Score={score} | Price={price:.2f} | RVOL={rvol:.2f}"
)

            if score >= 10:

                alerts.append(
                    f"""🚀 {symbol}

Score: {score}/100
Price: ${price:.2f}
RVOL: {rvol:.2f}

20 EMA: ${ema20:.2f}
50 EMA: ${ema50:.2f}

1M Return: {month_return:.1f}%"""
                )

        except Exception as e:
            print(f"{symbol} ERROR: {e}")

    if alerts:

        requests.post(
            WEBHOOK,
            json={"content": "\n\n".join(alerts)}
        )

        print("ALERT SENT")

    else:

        print("NO SIGNALS")

except Exception as e:

    print("FATAL ERROR:", e)
