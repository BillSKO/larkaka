import uuid
from datetime import datetime
from execution.trade_logger import _quick_log  # byts senare mot full logik

def place_binary_trade(platform, symbol, direction, amount, duration_seconds,
                       strategy, confidence, intent="binary_opportunity",
                       expected_pnl_pct=80.0, ai_signal=None):
    """
    Simulerar en binär trade (UP/DOWN). API-anrop implementeras per plattform.
    """

    trade_id = str(uuid.uuid4())
    entry_time = datetime.utcnow().isoformat()

    trade_data = {
        "id": trade_id,
        "platform": platform,
        "timestamp": entry_time,
        "symbol": symbol,
        "direction": direction,  # 'up' or 'down'
        "amount": amount,
        "duration_seconds": duration_seconds,
        "strategy": strategy,
        "confidence": confidence,
        "intent": intent,
        "expected_pnl_pct": expected_pnl_pct,
        "status": "pending",  # ändras till 'won' / 'lost' senare
        "ai_signal": ai_signal if ai_signal else {}
    }

    _quick_log(trade_data)
    print(f"[BINARY TRADE] {platform} {symbol} {direction.upper()} for {amount} | Duration: {duration_seconds}s")
    return trade_data
