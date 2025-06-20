# adapters/ccxt_adapter.py

import ccxt
from _api_keys import (
    BINANCE_API_KEY, BINANCE_API_SECRET,
    BYBIT_API_KEY, BYBIT_API_SECRET,
    BITGET_API_KEY, BITGET_API_SECRET, BITGET_API_PWD
)

class CCXTPriceFetcher:
    def __init__(self, exchange_name: str = "binance"):
        """
        Initierar ccxt-klienten med rätt API-nycklar.
        exchange_name: 'binance', 'bybit' eller 'bitget'
        """
        if exchange_name.lower() == "bybit":
            self.exchange = ccxt.bybit({
                'apiKey':    BYBIT_API_KEY,
                'secret':    BYBIT_API_SECRET
            })
        elif exchange_name.lower() == "bitget":
            self.exchange = ccxt.bitget({
                'apiKey':    BITGET_API_KEY,
                'secret':    BITGET_API_SECRET,
                'password':  BITGET_API_PWD
            })
        else:  # default: Binance
            self.exchange = ccxt.binance({
                'apiKey':    BINANCE_API_KEY,
                'secret':    BINANCE_API_SECRET
            })

        # Ladda marknader (måste anropas innan fetch)
        self.exchange.load_markets()

    def get_price(self, symbol: str):
        """
        Hämtar senaste pris för givet symbol, t.ex. "BTC/USDT".
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker.get("last")
        except Exception as e:
            print(f"[CCXT] Fel vid prisinhämtning för {symbol}: {e}")
            return None


def get_all_balances(exchange_name: str):
    """
    Hämtar totalbalance + detaljer för en exchange.
    Returnerar { total, currency, details } eller {"error": msg}.
    """
    try:
        if exchange_name.lower() == "binance":
            exchange = ccxt.binance({
                'apiKey':    BINANCE_API_KEY,
                'secret':    BINANCE_API_SECRET
            })
        elif exchange_name.lower() == "bybit":
            exchange = ccxt.bybit({
                'apiKey':    BYBIT_API_KEY,
                'secret':    BYBIT_API_SECRET
            })
        elif exchange_name.lower() == "bitget":
            exchange = ccxt.bitget({
                'apiKey':    BITGET_API_KEY,
                'secret':    BITGET_API_SECRET,
                'password':  BITGET_API_PWD
            })
        else:
            return {"error": f"Exchange '{exchange_name}' not supported"}

        # Hämta balans
        balances = exchange.fetch_balance()
        total    = balances.get('total', {})
        # Filtrera bort 0-värden
        positive = {cur: amt for cur, amt in total.items() if amt and amt > 0}
        total_sum = sum(positive.values())

        return {
            "total":    round(total_sum, 2),
            "currency": next(iter(positive), "EUR"),
            "details":  positive
        }

    except Exception as e:
        return {"error": str(e)}
