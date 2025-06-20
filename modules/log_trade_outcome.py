import os
import json
from datetime import datetime

FILEPATH = os.path.expanduser("~/NikolaDeploy/data/trade_outcome_log.json")
MAX_ENTRIES = 500

def log_trade_outcome(symbol, strategy, entry_price, exit_price, pnl, confidence, risk):
    try:
        success = "✅ PROFIT" if pnl > 0 else "❌ LOSS"

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "strategy": strategy,
            "entry_price": round(entry_price, 4),
            "exit_price": round(exit_price, 4),
            "pnl": round(pnl, 4),
            "result": success,
            "confidence": round(confidence * 100, 2),
            "risk": round(risk * 100, 2)
        }

        if os.path.exists(FILEPATH):
            try:
                with open(FILEPATH, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ JSON-fel i trade_outcome_log – filen nollställs")
                data = []
        else:
            data = []

        data.insert(0, log_entry)
        if len(data) > MAX_ENTRIES:
            data = data[:MAX_ENTRIES]

        with open(FILEPATH, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"❌ Kunde inte logga trade outcome: {e}")
