import random
import datetime
from ..app import log, update_status

def generate_ai_signal(symbol, exchange):
    # Simulerad AI-logik – ersätt med riktig ML eller API-integrering vid behov
    signal = random.choice(["BUY", "SELL", "HOLD"])
    confidence = round(random.uniform(0.6, 0.95), 2)
    reason = f"Simulated AI pattern match with {confidence * 100}% confidence."

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    signal_data = {
        "symbol": symbol,
        "exchange": exchange,
        "signal": signal,
        "confidence": confidence,
        "reason": reason,
        "time": timestamp
    }

    log(f"🧠 AI-signal genererad för {symbol} ({exchange}): {signal} ({confidence * 100}%)")
    update_status("ai_signal", signal_data)

    return signal_data
