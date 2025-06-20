import websocket
import threading
import json
import os
import time
from modules.deriv_status import get_deriv_balances

APP_ID = 80652
URL = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"

TOKEN_PATH_1 = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/token1.txt')  # Demo
TOKEN_PATH_2 = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/token2.txt')  # Real

def load_token(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[❌] Tokenfil saknas: {path}")
        return None

def send_trade_request(mode, symbol, contract_type, amount=1, duration=5):
    token_path = TOKEN_PATH_1 if mode == "demo" else TOKEN_PATH_2
    token = load_token(token_path)
    if not token:
        return

    def on_open(ws):
        print(f"[🔐] [{mode}] Autoriserar...")
        ws.send(json.dumps({"authorize": token}))

    def on_message(ws, message):
        data = json.loads(message)
        if data.get("msg_type") == "authorize":
            print(f"[✅] [{mode}] Inloggad: {data['authorize']['loginid']}")
            trade_req = {
                "buy": 1,
                "price": str(amount),
                "parameters": {
                    "amount": str(amount),
                    "basis": "stake",
                    "contract_type": contract_type,
                    "currency": "USD",
                    "duration": str(duration),
                    "duration_unit": "m",
                    "symbol": symbol
                },
                "subscribe": 0
            }
            ws.send(json.dumps(trade_req))
        elif data.get("msg_type") == "buy":
            print(f"[🎯] [{mode}] Trade skickad! ID: {data['buy']['transaction_id']}")
            ws.close()
        elif "error" in data:
            print(f"[❌] [{mode}] Fel: {data['error']['message']}")
            ws.close()

    def on_error(ws, error):
        print(f"[⚠️] [{mode}] WebSocket-fel:", error)

    def on_close(ws, code, reason):
        print(f"[🔌] [{mode}] Anslutning stängd.")

    ws = websocket.WebSocketApp(
        URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    thread = threading.Thread(target=ws.run_forever)
    thread.start()
    thread.join(timeout=15)
