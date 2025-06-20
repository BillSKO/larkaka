import ccxt
import json
import os

def load_bitget_keys():
    with open("/home/billskogsberg/NikolaWeb/config/keys.json") as f:
        keys = json.load(f)
    return keys.get("bitget", {})

def send_bitget_trade(symbol, side, amount):
    try:
        keys = load_bitget_keys()
        api_key = keys["apiKey"]
        secret = keys["secret"]
        password = keys["password"]

        exchange = ccxt.bitget({
            'apiKey': api_key,
            'secret': secret,
            'password': password,
            'enableRateLimit': True
        })

        markets = exchange.load_markets()
        if symbol not in markets:
            raise Exception(f"Symbol {symbol} not found on Bitget.")

        market = markets[symbol]
        price = exchange.fetch_ticker(symbol)["last"]

        order = exchange.create_market_order(symbol=symbol, side=side, amount=amount)

        return {
            "status": "success",
            "symbol": symbol,
            "side": side,
            "amount": amount,
            "price": price,
            "platform": "Bitget"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
