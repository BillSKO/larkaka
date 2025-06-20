import ccxt
import json
import os

def fetch_symbols():
    all_symbols = set()

    # Binance
    try:
        binance = ccxt.binance()
        binance.load_markets()
        all_symbols.update(binance.symbols)
    except Exception as e:
        print("⚠️ Binance fel:", e)

    # Bybit
    try:
        bybit = ccxt.bybit()
        bybit.load_markets()
        all_symbols.update(bybit.symbols)
    except Exception as e:
        print("⚠️ Bybit fel:", e)

    # Bitget
    try:
        bitget = ccxt.bitget()
        bitget.load_markets()
        all_symbols.update(bitget.symbols)
    except Exception as e:
        print("⚠️ Bitget fel:", e)

    filtered = sorted([s for s in all_symbols if "/" in s and "USDT" in s or "USD" in s])

    # Spara till whitelist
    os.makedirs("data", exist_ok=True)
    with open("data/symbol_whitelist.json", "w") as f:
        json.dump(filtered, f, indent=2)

    print(f"✅ Sparade {len(filtered)} symboler till data/symbol_whitelist.json")

if __name__ == "__main__":
    fetch_symbols()
