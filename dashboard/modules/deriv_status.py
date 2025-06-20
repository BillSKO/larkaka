import os
import json

STATUS_FILE = os.path.expanduser("~/NikolaWeb/data/deriv_status.json")

def save_deriv_status(data):
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_deriv_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def get_deriv_balances():
    data = load_deriv_status()
    balances = {}

    deriv_balance = data.get("balance", 0)
    currency = data.get("currency", "USD")
    connected = data.get("connected", False)

    balances["Deriv"] = {
        "balance": deriv_balance,
        "currency": currency,
        "connected": connected
    }

    return balances
