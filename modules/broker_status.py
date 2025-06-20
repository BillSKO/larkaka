import ccxt

def get_binance_balances(api_key, api_secret):
    try:
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret
        })
        balances = exchange.fetch_balance()['total']
        return {k: v for k, v in balances.items() if v > 0}
    except Exception as e:
        return {"error": str(e)}

def get_bybit_balances(api_key, api_secret):
    try:
        exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret
        })
        balances = exchange.fetch_balance()['total']
        return {k: v for k, v in balances.items() if v > 0}
    except Exception as e:
        return {"error": str(e)}

def get_bitget_balances(api_key, api_secret):
    try:
        exchange = ccxt.bitget({
            'apiKey': api_key,
            'secret': api_secret
        })
        balances = exchange.fetch_balance()['total']
        return {k: v for k, v in balances.items() if v > 0}
    except Exception as e:
        return {"error": str(e)}
