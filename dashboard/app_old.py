
from flask import Flask, jsonify, request, send_file
from flask_socketio import SocketIO, emit
import json
import datetime
import csv
from flask import Flask, jsonify, request, send_file
from flask_socketio import SocketIO
import json
import os
import datetime
from forex_python.converter import CurrencyRates

app = Flask(__name__)
socketio = SocketIO(app)

STATUS_FILE = "../data/nikola_live_status.json"
LOG_FILE = "../data/trade_log.txt"

def log(message):
    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_file.write(f"{timestamp} {message}\n")

def update_status(key, value):
    try:
        if not os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "w") as f:
                json.dump({}, f)

        with open(STATUS_FILE, "r") as f:
            status = json.load(f)

        status[key] = value

        with open(STATUS_FILE, "w") as f:
            json.dump(status, f, indent=4)

        socketio.emit("status_update", {key: value})
    except Exception as e:
        log(f"Fel vid statusuppdatering: {e}")

def convert_currency(amount, from_currency, to_currency="EUR"):
    try:
        c = CurrencyRates()
        rate = c.get_rate(from_currency.upper(), to_currency.upper())
        return amount * rate
    except Exception as e:
        log(f"Valutaomvandlingsfel: {e}")
        return amount

@app.route('/manual_trade', methods=['POST'])
def manual_trade():
    data = request.json

    exchange = data.get('exchange', 'binance')
    symbol = data.get('symbol', 'BTC/USDT')
    amount = float(data.get('amount', 0))
    currency = data.get('currency', 'SEK')
    risk = float(data.get('risk', 1.0))
    leverage = int(data.get('leverage', 1))

    converted = convert_currency(amount, currency)
    result = "+2.5%"  # Placeholder
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    strategy = "Manual"

    update_status("latest_trade", {
        "symbol": symbol,
        "result": result,
        "time": now
    })

    log(f"🔵 Manuell trade: {symbol} på {exchange} | {amount} {currency} ({converted:.2f} EUR) | Risk: {risk}, Leverage: {leverage}")

    return jsonify({
        "message": f"Trade skickad för {symbol} på {exchange}. Belopp: {converted:.2f} EUR (ursprungligen {amount} {currency})"
    })

@app.route('/get_status')
def get_status():
    try:
        with open(STATUS_FILE, 'r') as f:
            status = json.load(f)
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/log')
def get_log():
    try:
        return send_file(LOG_FILE, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/')
def index():
    return send_file("index.html")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5478)
