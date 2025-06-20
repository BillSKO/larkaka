from statistics import mean
from datetime import datetime
from modules.log_live_trade import log_live_trade
from modules.log_pnl import log_pnl

class CryptoSpreadStrategy:
    def __init__(self):
        self.spread_memory = []
        self.threshold = 0.005  # 0.5%

    def calculate_spread(self, price_a, price_b):
        if price_b == 0:
            return 0.0
        return round((price_a - price_b) / price_b, 5)

    def evaluate_spread(self, spreads):
        if len(spreads) < 10:
            return None, 0.0, 0.0

        current = spreads[-1]
        avg = mean(spreads[-10:])
        diff = current - avg

        confidence = min(1.0, abs(diff) * 100)
        risk = max(0.1, 1.0 - confidence)

        if diff > self.threshold:
            return "SELL BTC / BUY ETH", round(confidence, 2), round(risk, 2)
        elif diff < -self.threshold:
            return "BUY BTC / SELL ETH", round(confidence, 2), round(risk, 2)
        else:
            return None, 0.0, 0.0

    def run(self, symbol_a, symbol_b, prices_a, prices_b):
        if not prices_a or not prices_b or len(prices_a) != len(prices_b):
            return

        price_a = prices_a[-1]
        price_b = prices_b[-1]
        spread = self.calculate_spread(price_a, price_b)
        self.spread_memory.append(spread)

        # Håll max 100 spreads
        if len(self.spread_memory) > 100:
            self.spread_memory.pop(0)

        signal, confidence, risk = self.evaluate_spread(self.spread_memory)

        if signal:
            log = {
                "symbol": f"{symbol_a} vs {symbol_b}",
                "strategy": "Crypto Spread",
                "entry": spread,
                "risk": risk * 100,
                "confidence": confidence * 100,
                "profit": "0.00",
                "amount_factor": 1.0,
                "end_time": (datetime.utcnow()).isoformat()
            }

            try:
                log_live_trade(log)
                print(f"📈 Spread Signal: {signal} | Spread: {spread} | Conf: {confidence*100:.1f}% | Risk: {risk*100:.1f}%")
            except Exception as e:
                print(f"⚠️ Loggfel (spread trade): {e}")

            pnl = round(spread * 100, 2)
            try:
                log_pnl({
                    "symbol": f"{symbol_a} vs {symbol_b}",
                    "strategy": "Crypto Spread",
                    "pnl": pnl,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                print(f"⚠️ Loggfel (PnL): {e}")
