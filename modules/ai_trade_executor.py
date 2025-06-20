import os
import json
import time
from datetime import datetime
from executors.deriv_executor import send_deriv_trade
from executors.binance_executor import send_binance_trade
from executors.bybit_executor import send_bybit_trade
from executors.bitget_executor import send_bitget_trade  # ← NYTT
from utils.load_settings import load_settings

last_trade_time = 0

def execute_ai_signals():
    global last_trade_time
    settings = load_settings()
    cooldown = settings.get("timeout_seconds", 15)
    trade_amount = settings.get("amount", 100)
    active_markets = settings.get("selectedMarkets", {})

    ai_path = os.path.expanduser("~/NikolaWeb/data/ai_signals.json")
    if not os.path.exists(ai_path):
        return

    with open(ai_path, "r") as f:
        signals = json.load(f)[-5:]

    for signal in signals:
        ts = signal.get("timestamp")
        if not ts or already_traded(ts):
            continue

        platform = signal.get("platform", "deriv").lower()
        market = signal.get("market", "binary").lower()
        symbol = signal.get("symbol", "USD/JPY")

        if not active_markets.get(market, False):
            continue

        confidence = signal.get("confidence", 50)
        amount = adjust_amount(confidence, trade_amount)

        if time.time() - last_trade_time < cooldown:
            continue

        print(f"[AI] Executing signal on {platform} - {symbol} - {amount} SEK")

        if platform == "deriv":
            send_deriv_trade(symbol, amount, signal)
        elif platform == "binance":
            send_binance_trade(symbol, amount, signal)
        elif platform == "bybit":
            send_bybit_trade(symbol, amount, signal)
        elif platform == "bitget":
            send_bitget_trade(symbol, amount, signal)  # ← NYTT

        log_executed(ts)
        last_trade_time = time.time()
        break

def adjust_amount(confidence, base_amount):
    return round(base_amount * (confidence / 100))

def already_traded(ts):
    path = os.path.expanduser("~/NikolaWeb/data/trade_timestamps.log")
    if os.path.exists(path):
        with open(path, "r") as f:
            if ts in f.read():
                return True
    return False

def log_executed(ts):
    path = os.path.expanduser("~/NikolaWeb/data/trade_timestamps.log")
    with open(path, "a") as f:
        f.write(f"{ts}\n")
