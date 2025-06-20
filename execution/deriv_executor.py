import websocket
import json
import uuid
import os
from datetime import datetime
from execution.trade_logger import _quick_log

TOKEN_PATH = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/token1.txt')
DERIV_WS_URL = "wss://ws.deriv.com/websockets/v3"

def load_token():
    with open(TOKEN_PATH, 'r') as f:
        return f.read().strip()

def place_binary_trade(symbol, amount, direction, duration, strategy, confidence,
                       intent="deriv_binary_trade", expected_pnl_pct=85.0, ai_signal=None):
    token = load_token()
    ws = websocket.create_connection(DERIV_WS_URL)

    # 1. Authorize
    auth_req = {"authorize": token}
    ws.send(json.dumps(auth_req))
    auth_res = json.loads(ws.recv())
    if 'error' in auth_res:
        print("[DERIV ERROR] Auth failed:", auth_res['error']['message'])
        ws.close()
        return None

    # 2. Buy contract
    contract_type = "CALL" if direction == "up" else "PUT"
    proposal_req = {
        "buy": 1,
        "price": amount,
        "parameters": {
            "amount": amount,
            "basis": "stake",
            "contract_type": contract_type,
            "currency": "USD",
            "duration": duration,
            "duration_unit": "s",
            "symbol": symbol
        }
    }
    ws.send(json.dumps(proposal_req))
    result = json.loads(ws.recv())

    if "error" in result:
        print("[DERIV ERROR] Trade failed:", result['error']['message'])
        ws.close()
        return None

    buy_info = result.get("buy")
    trade_id = str(uuid.uuid4())
    trade_data = {
        "id": trade_id,
        "platform": "Deriv",
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "direction": direction,
        "amount": amount,
        "duration_seconds": duration,
        "strategy": strategy,
        "confidence": confidence,
        "intent": intent,
        "expected_pnl_pct": expected_pnl_pct,
        "status": "pending",
        "contract_id": buy_info.get("contract_id"),
        "ai_signal": ai_signal if ai_signal else {}
    }

    _quick_log(trade_data)
    print(f"[DERIV TRADE] {symbol} {direction.upper()} for {amount} USD | Contract: {buy_info.get('contract_id')}")
    ws.close()
    return trade_data
