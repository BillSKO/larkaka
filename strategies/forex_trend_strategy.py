from datetime import datetime
from nikola_core import log_pnl
from modules.log_live_trade import log_live_trade

class ForexTrendStrategy:
    def __init__(self):
        self.trades = {}
        self.min_data = 15
        self.exit_threshold = 0.005  # 0.5% rörelse räcker för exit

    def detect_trend(self, prices):
        if len(prices) < self.min_data:
            return None, 0.0, 0.0

        short_avg = sum(prices[-5:]) / 5
        long_avg = sum(prices[-10:]) / 10
        diff = short_avg - long_avg

        strength = abs(diff / long_avg)
        confidence = round(min(strength * 2, 1.0), 2)
        risk = round(1.0 - confidence, 2)

        if diff > 0.0003:
            return "buy", confidence, risk
        elif diff < -0.0003:
            return "sell", confidence, risk
        return None, 0.0, 0.0

    def enter_trade(self, symbol, price, signal, confidence, risk):
        if symbol in self.trades:
            print(f"↩️ Redan öppen position i {symbol}, ignorerar ny trade.")
            return

        self.trades[symbol] = {
            "entry": price,
            "strategy": "ForexTrendStrategy",
            "signal": signal,
            "confidence": confidence,
            "risk": risk,
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            log_live_trade(
                symbol=symbol,
                strategy="ForexTrendStrategy",
                entry_price=price,
                confidence=confidence,
                risk=risk
            )
        except Exception as e:
            print(f"⚠️ Kunde inte logga live trade: {e}")

        print(f"🔔 Entered {signal.upper()} on {symbol} at {price:.4f} | Conf: {confidence*100:.1f}%, Risk: {risk*100:.1f}%")

    def check_exit(self, symbol, current_price):
        if symbol not in self.trades:
            return None, 0.0, None, 0.0, 0.0

        trade = self.trades[symbol]
        entry = trade["entry"]
        direction = trade["signal"]
        delta = (current_price - entry) / entry if direction == "buy" else (entry - current_price) / entry

        if delta >= self.exit_threshold:
            pnl = round((current_price - entry) if direction == "buy" else (entry - current_price), 4)
            try:
                log_pnl(symbol, trade["strategy"], pnl)
                print(f"💰 Closed {symbol} | PnL: {pnl:.4f}")
            except Exception as e:
                print(f"⚠️ Kunde inte logga PnL: {e}")

            del self.trades[symbol]
            return entry, pnl, direction, trade["confidence"], trade["risk"]

        return entry, 0.0, direction, trade["confidence"], trade["risk"]

    def run(self, symbol, price_data, mode="demo"):
        current_price = price_data[-1]
        signal, confidence, risk = self.detect_trend(price_data)

        if symbol in self.trades:
            return self.check_exit(symbol, current_price)

        elif signal:
            self.enter_trade(symbol, current_price, signal, confidence, risk)
            return current_price, 0.0, signal, confidence, risk

        return current_price, 0.0, None, 0.0, 0.0
