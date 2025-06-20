import websocket
import threading
import json
import os

APP_ID = 80652
URL = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"

TOKEN_PATH_1 = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/token1.txt')  # Demo
TOKEN_PATH_2 = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/token2.txt')  # Real

def load_token(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[❌] Token saknas: {path}")
        return None

def get_deriv_balances():
    result = {}

    def connect(token, label):
        def on_message(ws, message):
            data = json.loads(message)
            if data.get("msg_type") == "authorize":
                acc = data["authorize"]
                result[label] = {
                    "loginid": acc.get("loginid", ""),
                    "balance": acc.get("balance", 0),
                    "currency": acc.get("currency", "N/A"),
                    "is_virtual": acc.get("is_virtual", 1)
                }
            ws.close()

        def on_open(ws):
            ws.send(json.dumps({"authorize": token}))

        ws = websocket.WebSocketApp(URL, on_open=on_open, on_message=on_message)
        ws.run_forever()

    threads = []
    for path, label in [(TOKEN_PATH_1, "demo"), (TOKEN_PATH_2, "live")]:
        token = load_token(path)
        if token:
            t = threading.Thread(target=connect, args=(token, label))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    return result
