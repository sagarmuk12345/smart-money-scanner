import yfinance as yf

print("STARTING SCANNER")

with open("watchlist.txt") as f:
    symbols = [line.strip() for line in f]

print(f"Loaded {len(symbols)} symbols")

for symbol in symbols:

    try:

        print(f"Checking {symbol}")

        stock = yf.Ticker(symbol)

        hist = stock.history(period="1mo")

        print(f"Rows: {len(hist)}")

        avg_volume = hist["Volume"].tail(20).mean()

        latest_volume = hist["Volume"].iloc[-1]

        rvol = latest_volume / avg_volume

        print(f"{symbol} | RVOL = {rvol:.2f}")

    except Exception as e:

        print(f"ERROR {symbol}: {e}")

print("SCANNER COMPLETE")
