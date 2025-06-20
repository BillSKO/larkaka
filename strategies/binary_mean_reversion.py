from datetime import datetime, timedelta
from statistics import mean, stdev
from modules.log_live_trade import log_live_trade
from modules.log_pnl import log_pnl

class BinaryMeanReversionStrategy:
    def __init__(self):
        self.active_trades = {}

    def calculate_z_score(self, price_data):
        if len(price_data) < 20:
            return 0.0
        avg = mean(price_data[-20:])
        std = stdev(price_data[-20:])
        current = price_data[-1]
        return (current - avg) / std if std != 0 else 0.0

    def calculate_confidence_and_risk(self, z):
        abs_z = abs(z)
        confidence = min(1.0, 0.65 + abs_z * 0.25)
        risk = max(0.05, 1.0 - confidence)
        return round(confidence, 2), round(risk, 2)

    def low_volatility(self, price_data, threshold=0.002):
        if len(price_data) < 20:
            return True
        avg = mean(price_data[-20:])
        std = stdev(price_data[-20:])
        return std / avg < threshold

    def generate_signal(self, symbol, price_data):
        if self.low_volatility(price_data):
            return None, 0.0, 0.0

        z = self.calculate_z_score(price_data)
        confidence, risk = self.calculate_confidence_and_risk(z)

        if z <= -1.25:
            return "UP", confidence, risk
        elif z >= 1.25:
            return "DOWN", confidence, risk
        else:
            return None, 0.0, 0.0

    def enter_trade(self, symbol, price, strategy_name="binary_mean_reversion", signal="UP", confidence=0.7, risk=0.4):
        end_time = datetime.utcnow() + timedelta(minutes=1)

        self.active_trades[symbol] = {
            "entry": price,
            "strategy": strategy_name,
            "end_time": end_time,
            "direction": signal
        }

        try:
            log_live_trade({
                "symbol": symbol,
                "strategy": strategy_name,
                "entry": price,
                "risk": risk * 100,
                "confidence": confidence * 100,
                "profit": "0.00",
                "amount_factor": 1.0,
                "end_time": end_time.isoformat()
            })
        except Exception as e:
            print(f"⚠️ Loggfel (live trade): {e}")

        print(f"🚀 Entered {symbol} @ {price} | {signal} | Confidence: {confidence*100:.1f}% | Risk: {risk*100:.1f}%")

    def check_exit(self, symbol, current_price):
        if symbol not in self.active_trades:
            return

        trade = self.active_trades[symbol]
        entry = trade["entry"]
        strategy = trade["strategy"]
        end_time = trade["end_time"]
        direction = trade["direction"]

        # Exit på tid eller SL/TP
        hit_tp = direction == "UP" and current_price > entry * 1.005
        hit_tp |= direction == "DOWN" and current_price < entry * 0.995
        hit_sl = direction == "UP" and current_price < entry * 0.9975
        hit_sl |= direction == "DOWN" and current_price > entry * 1.0025
        time_up = datetime.utcnow() >= end_time

        if hit_tp or hit_sl or time_up:
            pnl = round(current_price - entry, 4)
            try:
                log_pnl({
                    "symbol": symbol,
                    "strategy": strategy,
                    "pnl": pnl,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                print(f"⚠️ Loggfel (PnL): {e}")

            print(f"✅ Closed {symbol} | Exit reason: {'TP' if hit_tp else 'SL' if hit_sl else 'TIME'} | PnL: {pnl}")
            del self.active_trades[symbol]

    def run(self, symbol, price_data, mode="demo"):
        if not price_data or len(price_data) < 20:
            return

        current_price = price_data[-1]
        signal, confidence, risk = self.generate_signal(symbol, price_data)

        if symbol in self.active_trades:
            self.check_exit(symbol, current_price)
        elif signal:
            self.enter_trade(symbol, current_price, signal=signal, confidence=confidence, risk=risk)
