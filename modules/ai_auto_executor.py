import os
import time
import json
from datetime import datetime
from pathlib import Path
from modules.deriv_api import send_trade_request
from modules.log_live_trade import log_live_trade
from modules.log_pnl import log_pnl
from app import load_mode

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
executed_signals = set()

def get_new_ai_signals():
    filepath = DATA_DIR / "ai_signals.json"
    if not filepath.exists():
        return []

    with open(filepath, "r") as f:
        signals = json.load(f)

    new_signals = []
    for signal in signals:
        sig_id = signal.get("id") or signal.get("timestamp")  # Unikt ID
        if sig_id not in executed_signals:
            executed_signals.add(sig_id)
            new_signals.append(signal)
    return new_signals

def run_signal_executor():
    print("AI-signal-exekvering startad...")
    while True:
        mode = load_mode()
        is_demo = mode.get("demo", True)

        new_signals = get_new_ai_signals()
        for signal in new_signals:
            trade = {
                "symbol": signal.get("symbol"),
                "direction": signal.get("direction", "UP"),
                "amount": 100,
                "platform": "Deriv",
                "strategy": signal.get("strategy", "AI"),
                "confidence": signal.get("confidence", 50),
                "timestamp": datetime.utcnow().isoformat()
            }

            result = send_trade_request(trade, is_demo=is_demo)
            trade.update(result)
            log_live_trade(trade)
            log_pnl(trade)

            print("Trade skickad:", trade)

        time.sleep(5)
