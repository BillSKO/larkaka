import websocket
import json
import os
import threading

app_id = 80652
url = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"

token1_path = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/token1.txt')
token2_path = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/token2.txt')

with open(token1_path, 'r') as f:
    token1 = f.read().strip()
with open(token2_path, 'r') as f:
    token2 = f.read().strip()

def run_test(token, label):
    def on_message(ws, message):
        data = json.loads(message)
        print(f"\n📩 [{label}] Svar:")
        print(json.dumps(data, indent=2))
        ws.close()

    def on_error(ws, error):
        print(f"❌ [{label}] WebSocket-fel:", error)

    def on_close(ws, close_status_code, close_msg):
        print(f"🔌 [{label}] Anslutningen stängdes.")

    def on_open(ws):
        print(f"🔐 [{label}] Skickar autorisation...")
        ws.send(json.dumps({
            "authorize": token
        }))

    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()

t1 = threading.Thread(target=run_test, args=(token1, "Konto 1"))
t2 = threading.Thread(target=run_test, args=(token2, "Konto 2"))

t1.start()
t2.start()

t1.join()
t2.join()
