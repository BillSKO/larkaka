from nikola_core import log_pnl, log_live_trade

class BaseStrategy:
    def __init__(self):
        self.trades = {}

    def generate_signal(self, symbol, price_data):
        print(f"⚠️ [BASE] generate_signal() måste implementeras för {symbol}")
        return None

    def enter_trade(self, symbol, price, strategy_name="BaseStrategy"):
        self.trades[symbol] = {
            "entry": price,
            "strategy": strategy_name
        }

        risk = 0.5
        confidence = 0.5

        try:
            log_live_trade(
                symbol=symbol,
                strategy=strategy_name,
                entry_price=price,
                risk=risk,
                confidence=confidence
            )
        except Exception as e:
            print(f"⚠️ Kunde inte logga live trade: {e}")

        print(f"🔧 [BASE] Entered trade on {symbol} at {price}")

    def check_exit(self, symbol, current_price):
        if symbol not in self.trades:
            return

        entry = self.trades[symbol]["entry"]
        strategy = self.trades[symbol]["strategy"]

        if abs(current_price - entry) >= 1.0:
            pnl = round(current_price - entry, 2)
            log_pnl(symbol, strategy, pnl)
            print(f"✅ [BASE] Closed trade on {symbol} | PnL: {pnl}")
            del self.trades[symbol]

    def run(self, symbol, price_data):
        current_price = price_data[-1] if price_data else None
        signal = self.generate_signal(symbol, price_data)

        if current_price is None:
            return

        if symbol in self.trades:
            self.check_exit(symbol, current_price)
        elif signal:
            self.enter_trade(symbol, current_price)
