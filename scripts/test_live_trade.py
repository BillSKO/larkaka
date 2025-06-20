import json
from datetime import datetime, timedelta

trade_log = {
    "symbol": "BTC/USDT",
    "strategy": "TestStrategy",
    "entry": 26450.0,
    "risk": 2.5,
    "confidence": 92.0,
    "potential_profit": 47.2,
    "profit": "12.5$",
    "amount_factor": 1.92,
    "end_time": (datetime.utcnow() + timedelta(minutes=5)).isoformat()
}

with open("data/live_trades.json", "w") as f:
    json.dump([trade_log], f, indent=2)

print("✅ Test trade loggad")
