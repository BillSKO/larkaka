import ccxt
import json
import os
import uuid
from datetime import datetime
from execution.trade_logger import _quick_log  # tillfälligt, ersätts senare

# Ladda API-nycklar
with open(os.path.expanduser('~/NikolaWeb/config/keys.json')) as f:
    keys = json.load(f)
bitget_keys = keys['bitget']

# Initiera Bitget med password
exchange = ccxt.bitget({
    'apiKey': bitget_keys['apiKey'],
    'secret': bitget_keys['secret'],
    'password': bitget_keys['password'],
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})


def place_order(symbol, side, amount, strategy, confidence,
                intent="default_strategy", tp_pct=2.0, sl_pct=1.0,
                expected_pnl_pct=3.0, expected_holding_minutes=10,
                ai_signal=None):
    try:
        order = exchange.create_market_order(symbol, side, amount)
        entry_price = order['average'] or order['price']

        tp_price = round(entry_price * (1 + tp_pct / 100), 6) if side == 'buy' else round(entry_price * (1 - tp_pct / 100), 6)
        sl_price = round(entry_price * (1 - sl_pct / 100), 6) if side == 'buy' else round(entry_price * (1 + sl_pct / 100), 6)

        trade_id = str(uuid.uuid4())

        trade_data = {
            "id": trade_id,
            "platform": "Bitget",
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "side": side,
            "amount": amount,
            "strategy": strategy,
            "confidence": confidence,
            "entry_price": entry_price,
            "tp_price": tp_price,
            "sl_price": sl_price,
            "expected_pnl_pct": expected_pnl_pct,
            "expected_holding_minutes": expected_holding_minutes,
            "intent": intent,
            "status": "open",
            "ai_signal": ai_signal if ai_signal else {}
        }

        _quick_log(trade_data)
        print(f"[BITGET TRADE] {symbol} {side} @ {entry_price} | TP: {tp_price} | SL: {sl_price}")
        return trade_data

    except Exception as e:
        print(f"[BITGET ERROR] Order failed: {e}")
        return None
