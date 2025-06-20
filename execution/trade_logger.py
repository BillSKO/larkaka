import json
import os
from datetime import datetime

LIVE_TRADES_PATH = os.path.expanduser('~/NikolaWeb/data/live_trades.json')
TRADE_HISTORY_PATH = os.path.expanduser('~/NikolaWeb/data/trade_history.json')
PNL_LOG_PATH = os.path.expanduser('~/NikolaWeb/data/pnl_log.json')


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)


def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def update_trade_status(trade_id, final_price, close_reason="manual", close_time=None):
    trades = load_json(LIVE_TRADES_PATH)
    history = load_json(TRADE_HISTORY_PATH)
    pnl_log = load_json(PNL_LOG_PATH)

    updated = False
    for trade in trades:
        if trade.get("id") == trade_id:
            trade["exit_price"] = final_price
            trade["status"] = "closed"
            trade["exit_time"] = close_time or datetime.utcnow().isoformat()
            trade["close_reason"] = close_reason

            # PnL
            entry = trade["entry_price"]
            amount = trade["amount"]
            side = trade["side"]
            if side == "buy":
                pnl = (final_price - entry) * amount
                pnl_pct = ((final_price - entry) / entry) * 100
            else:
                pnl = (entry - final_price) * amount
                pnl_pct = ((entry - final_price) / entry) * 100

            trade["pnl"] = round(pnl, 4)
            trade["pnl_pct"] = round(pnl_pct, 2)

            pnl_log.append({
                "id": trade_id,
                "symbol": trade["symbol"],
                "strategy": trade["strategy"],
                "timestamp": trade["exit_time"],
                "pnl": round(pnl, 4),
                "pnl_pct": round(pnl_pct, 2)
            })

            history.append(trade)
            trades.remove(trade)
            updated = True
            break

    if updated:
        save_json(trades, LIVE_TRADES_PATH)
        save_json(history, TRADE_HISTORY_PATH)
        save_json(pnl_log, PNL_LOG_PATH)
        print(f"[TRADE CLOSED] {trade_id} | PnL: {pnl} ({pnl_pct}%)")
    else:
        print(f"[ERROR] Trade ID {trade_id} not found.")


def get_open_trades():
    return load_json(LIVE_TRADES_PATH)
