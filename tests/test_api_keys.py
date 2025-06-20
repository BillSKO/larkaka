import ccxt
import json
import os

with open(os.path.expanduser('~/NikolaWeb/config/keys.json')) as f:
    keys = json.load(f)

exchanges = {
    "binance": ccxt.binance,
    "bybit": ccxt.bybit,
    "bitget": ccxt.bitget
}

for name, client in exchanges.items():
    print(f"\n== Testing {name.upper()} ==")
    try:
        apiKey = keys[name]["apiKey"]
        secret = keys[name]["secret"]

        creds = {
            'apiKey': apiKey,
            'secret': secret,
            'enableRateLimit': True
        }

        # Lägg till password för Bitget
        if name == "bitget":
            creds['password'] = keys[name]["password"]

        exchange = client(creds)

        balance = exchange.fetch_balance()
        print("✅ Connection OK | Sample balance:", {k: v for k, v in balance['total'].items() if v})
    except Exception as e:
        print(f"❌ ERROR connecting to {name.upper()}: {e}")
