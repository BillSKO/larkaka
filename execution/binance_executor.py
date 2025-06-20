import ccxt
import json
import os
import uuid
from datetime import datetime

# Ladda nycklar
with open(os.path.expanduser('~/NikolaWeb/config/keys.json')) as f:
    keys = json.load(f)
binance_keys = keys['binance']

# Initiera exchange
exchange = ccxt.binance({
    'apiKey': binance_keys['apiKey'],
    'secret': binance_keys['secret'],
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

def place_order(symbol, side, amount, strategy, confidence,
                intent="default_strategy", tp_pct=2.0, sl_pct=1.0,
                expected_pnl_pct=3.0, expected_holding_minutes=10,
                ai_signal=None):
    try:
        # Skapa order
        order = exchange.create_market_order(symbol, side, amount)
        entry_price = order['average'] or order['price']

        # Beräkna TP/SL-nivåer
        tp_price = round(entry_price * (1 + tp_pct / 100), 6) if side == 'buy' else round(entry_price * (1 - tp_pct / 100), 6)
        sl_price = round(entry_price * (1 - sl_pct / 100), 6) if side == 'buy' else round(entry_price * (1 + sl_pct / 100), 6)

        # Skapa unik ID
        trade_id = str(uuid.uuid4())

        # Struktur för trade
        trade_data = {
            "id": trade_id,
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

        # Tillfällig direktloggning – byts ut till trade_logger.py
        _quick_log(trade_data)

        print(f"[TRADE EXECUTED] {symbol} {side} @ {entry_price} | TP: {tp_price}, SL: {sl_price}")
        return trade_data

    except Exception as e:
        print(f"[ERROR] Order failed: {e}")
        return None

# Enkel loggning innan vi bygger trade_logger.py
def _quick_log(trade_data):
    filepath = os.path.expanduser('~/NikolaWeb/data/live_trades.json')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
        else:
            data = []

        data.append(trade_data)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Could not write log: {e}")
