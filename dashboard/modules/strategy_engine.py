import random
from datetime import datetime

def select_strategy(symbol):
    """
    Enkel logik för demo. Ersätt med riktiga AI-beslut senare.
    """
    strategies = ["Mean Reversion", "Breakout", "Trend Follow"]
    selected = random.choice(strategies)
    confidence = round(random.uniform(0.6, 0.95), 2)
    recommended_amount = round(random.uniform(50, 200), 2)
    stop_loss = round(random.uniform(1.5, 3.5), 2)
    take_profit = round(random.uniform(2.5, 6.0), 2)

    return {
        "symbol": symbol,
        "strategy": selected,
        "confidence": confidence,
        "amount": recommended_amount,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "time": datetime.now().isoformat()
    }
