import websocket
import json
import os

TOKEN_PATH = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/token1.txt')
DERIV_WS_URL = "wss://ws.binaryws.com/websockets/v3"

def load_token():
    try:
        with open(TOKEN_PATH, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("[❌] Tokenfil saknas:", TOKEN_PATH)
        exit(1)

def test_deriv_connection():
    token = load_token()

    try:
        ws = websocket.create_connection(DERIV_WS_URL)
    except Exception as e:
        print(f"[❌] WebSocket Connection Failed: {e}")
        return

    # Skicka endast token (ingen app_id behövs vid OAuth)
    ws.send(json.dumps({"authorize": token}))
    auth_res = json.loads(ws.recv())
    if "error" in auth_res:
        print("[❌] AUTH ERROR:", auth_res['error']['message'])
        return

    user = auth_res["authorize"]["loginid"]

    ws.send(json.dumps({"balance": 1}))
    balance_res = json.loads(ws.recv())
    balance = balance_res["balance"]["balance"]

    print(f"[✅] Deriv Connected as {user} | Balance: {balance:.2f} USD")

    ws.send(json.dumps({"active_symbols": "brief", "product_type": "basic"}))
    symbols_res = json.loads(ws.recv())

    print(f"\n[📊] Available symbols:")
    for sym in symbols_res.get("active_symbols", []):
        print(f"- {sym['symbol']} ({sym['display_name']})")

    ws.close()

if __name__ == "__main__":
    test_deriv_connection()
