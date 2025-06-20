import time
import ccxt
import json
import os
from execution.trade_logger import update_trade_status, get_open_trades

# Hämta API-nycklar
with open(os.path.expanduser('~/NikolaWeb/config/keys.json')) as f:
    keys = json.load(f)

binance_keys = keys['binance']

exchange = ccxt.binance({
    'apiKey': binance_keys['apiKey'],
    'secret': binance_keys['secret'],
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

def get_current_price(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"[ERROR] Could not fetch price for {symbol}: {e}")
        return None

def monitor_loop(interval=5):
    print("[MONITOR] Starting PnL monitor...")
    while True:
        trades = get_open_trades()
        for trade in trades:
            symbol = trade["symbol"]
            side = trade["side"]
            tp = trade["tp_price"]
            sl = trade["sl_price"]
            trade_id = trade["id"]

            price = get_current_price(symbol)
            if not price:
                continue

            if side == "buy":
                if price >= tp:
                    update_trade_status(trade_id, price, close_reason="tp_hit")
                elif price <= sl:
                    update_trade_status(trade_id, price, close_reason="sl_hit")
            elif side == "sell":
                if price <= tp:
                    update_trade_status(trade_id, price, close_reason="tp_hit")
                elif price >= sl:
                    update_trade_status(trade_id, price, close_reason="sl_hit")

        time.sleep(interval)
