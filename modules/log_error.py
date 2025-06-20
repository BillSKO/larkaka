import os
import json
from datetime import datetime
import traceback

MAX_ENTRIES = 300
FILEPATH = os.path.expanduser("~/NikolaDeploy/data/error_log.json")

def log_error(error_message, module="unknown", details=None):
    try:
        error_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "module": module,
            "error": str(error_message),
            "trace": traceback.format_exc(),
            "details": details or "-"
        }

        if os.path.exists(FILEPATH):
            try:
                with open(FILEPATH, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ JSON-fel – nollställer error_log.json")
                data = []
        else:
            data = []

        data.insert(0, error_entry)
        if len(data) > MAX_ENTRIES:
            data = data[:MAX_ENTRIES]

        with open(FILEPATH, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"❌ Kritisk loggningsmiss: {e}")
