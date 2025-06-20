import json
from datetime import datetime, timedelta

ai_signal = {
    "platform": "Binance",
    "symbol": "BTC/USDT",
    "strategy": "TestStrategy",
    "risk": 3.2,
    "confidence": 91.4,
    "eta": (datetime.utcnow() + timedelta(minutes=5)).isoformat(),
    "duration": "00:05:00"
}

with open("data/ai_signals.json", "w") as f:
    json.dump([ai_signal], f, indent=2)

print("✅ Testsignal skapad")
