from flask import Flask, render_template, jsonify, request
import os, json, requests, sys
from datetime import datetime
from pathlib import Path

# Lägg till path så adapters funkar
sys.path.insert(0, "/home/billskogsberg/NikolaWeb")

from modules.deriv_status import get_deriv_balances
from adapters.ccxt_adapter import get_all_balances

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))

EXCHANGE_API = "https://open.er-api.com/v6/latest/USD"

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return []

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
@app.route("/api/data")
def api_data():
    currency = request.args.get("currency", "EUR")

    fx_rate = get_fx_rate(currency)
    system_status = load_json(DATA_DIR / "system_status.json")
    pnl_log = load_json(DATA_DIR / "pnl_log.json")
    live_trades = load_json(DATA_DIR / "live_trades.json")
    ai_signals = load_json(DATA_DIR / "ai_signals.json")
    trade_outcomes = load_json(DATA_DIR / "trade_history.json")

    deriv_balances = get_deriv_balances()
    ccxt_balances = get_all_balances()

    market_settings = load_json(DATA_DIR / "market_settings.json")
    if not market_settings:
        market_settings = {"crypto": False, "forex": False, "binary": False}

    current_balances = []
    for exch, val in deriv_balances.items():
        current_balances.append({"platform": exch, "balance": round(val["balance"] * fx_rate, 2), "currency": currency})
    for exch, val in ccxt_balances.items():
        current_balances.append({"platform": exch, "balance": round(val["balance"] * fx_rate, 2), "currency": currency})

    total_profit, total_loss = 0, 0
    pnl_labels, pnl_values = [], []

    for row in pnl_log[-50:]:
        profit = row.get("profit", 0) * fx_rate
        pnl_labels.append(row.get("time", ""))
        pnl_values.append(profit)
        if profit >= 0:
            total_profit += profit
        else:
            total_loss += abs(profit)

    overall_result = total_profit - total_loss
    return jsonify({
        "nikola_active": system_status.get("nikola_active", False),
        "binance_status": ccxt_balances.get("Binance", {}).get("connected", False),
        "bybit_status": ccxt_balances.get("Bybit", {}).get("connected", False),
        "bitget_status": ccxt_balances.get("Bitget", {}).get("connected", False),
        "deriv_status": deriv_balances.get("Deriv", {}).get("connected", False),
        "markets": market_settings,
        "live_trades": live_trades,
        "ai_signals": ai_signals,
        "trade_outcomes": trade_outcomes,
        "balances": current_balances,
        "profit": round(total_profit, 2),
        "loss": round(total_loss, 2),
        "overall": round(overall_result, 2),
        "pnl_chart": {"labels": pnl_labels, "values": pnl_values}
    })
@app.route("/api/control/<cmd>", methods=["POST"])
def control(cmd):
    status_file = DATA_DIR / "system_status.json"
    status = load_json(status_file)
    if not status:
        status = {"nikola_active": False}

    if cmd == "start":
        status["nikola_active"] = True
    elif cmd == "stop":
        status["nikola_active"] = False

    save_json(status_file, status)
    return jsonify({"status": "ok", "nikola_active": status["nikola_active"]})


@app.route("/api/update_markets", methods=["POST"])
def update_markets():
    content = request.json
    settings_file = DATA_DIR / "market_settings.json"
    settings = load_json(settings_file)
    if not settings:
        settings = {"crypto": False, "forex": False, "binary": False}

    market = content.get("market")
    active = content.get("active", False)
    if market in settings:
        settings[market] = active

    save_json(settings_file, settings)
    return jsonify({"status": "ok", "markets": settings})
