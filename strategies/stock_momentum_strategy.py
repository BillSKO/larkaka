from datetime import datetime
from nikola_core import log_pnl
from modules.log_live_trade import log_live_trade

class StockMomentumStrategy:
    def __init__(self):
        self.active_trades = {}
        self.window = 6
        self.base_threshold = 0.003  # 0.3%

    def generate_signal(self, symbol, price_data):
        if len(price_data) < self.window + 1:
            print(f"📉 För lite data för {symbol} – behövs minst {self.window + 1} punkter.")
            return None, 0.0, 0.0

        prev_price = price_data[-self.window - 1]
        current_price = price_data[-1]

        change_pct = (current_price - prev_price) / prev_price
        confidence = round(min(abs(change_pct * 15), 1.0), 2)
        risk = round(1.0 - confidence, 2)

        if change_pct >= self.base_threshold:
            return "buy", confidence, risk
        elif change_pct <= -self.base_threshold:
            return "sell", confidence, risk
        return None, 0.0, 0.0

    def enter_trade(self, symbol, price, signal, confidence, risk):
        if symbol in self.active_trades:
            print(f"⚠️ Redan en aktiv trade för {symbol}.")
            return price, 0.0, signal, confidence, risk

        self.active_trades[symbol] = {
            "entry": price,
            "strategy": "StockMomentum",
            "confidence": confidence,
            "risk": risk,
            "signal": signal,
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            log_live_trade(
                symbol=symbol,
                strategy="StockMomentum",
                entry_price=price,
                risk=risk,
                confidence=confidence
            )
        except Exception as e:
            print(f"⚠️ Kunde inte logga live trade: {e}")

        print(f"📈 Entered {signal.upper()} on {symbol} @ {price:.2f} | Conf: {confidence*100:.1f}%, Risk: {risk*100:.1f}%")
        return price, 0.0, signal, confidence, risk

    def check_exit(self, symbol, current_price):
        if symbol not in self.active_trades:
            return None, 0.0, None, 0.0, 0.0

        trade = self.active_trades[symbol]
        entry = trade["entry"]
        signal = trade["signal"]
        direction_multiplier = 1 if signal == "buy" else -1
        pnl = round(direction_multiplier * (current_price - entry), 4)

        threshold = entry * 0.006  # 0.6%
        if abs(current_price - entry) >= threshold:
            try:
                log_pnl(symbol, trade["strategy"], pnl)
                print(f"✅ EXIT {symbol} | PnL: {pnl:.4f}")
            except Exception as e:
                print(f"⚠️ Kunde inte logga PnL: {e}")

            del self.active_trades[symbol]
            return entry, pnl, signal, trade["confidence"], trade["risk"]

        return entry, 0.0, signal, trade["confidence"], trade["risk"]

    def run(self, symbol, price_data, mode="demo"):
        current_price = price_data[-1]
        signal, confidence, risk = self.generate_signal(symbol, price_data)

        if symbol in self.active_trades:
            return self.check_exit(symbol, current_price)

        elif signal:
            return self.enter_trade(symbol, current_price, signal, confidence, risk)

        return current_price, 0.0, None, 0.0, 0.0
