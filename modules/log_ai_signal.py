import os
import json
from datetime import datetime

SIGNAL_PATH = os.path.expanduser("~/NikolaWeb/dashboard/data/ai_signals.json")
MAX_ENTRIES = 500

def log_ai_signal(signal):
    try:
        if "timestamp" not in signal:
            signal["timestamp"] = datetime.utcnow().isoformat()

        if os.path.exists(SIGNAL_PATH):
            try:
                with open(SIGNAL_PATH, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ JSON-fel – nollställer ai_signals.json")
                data = []
        else:
            data = []

        data.insert(0, signal)

        if len(data) > MAX_ENTRIES:
            data = data[:MAX_ENTRIES]

        with open(SIGNAL_PATH, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"❌ Fel vid loggning av AI-signal: {e}")
