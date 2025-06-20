import random
from datetime import datetime

def scan_market():
    """
    Simulerad marknadsskanning – byt ut mot riktiga API-anrop sen.
    """
    symbols = ["BTC/USDT", "ETH/USDT", "EUR/USD", "XAU/USD", "SOL/USDT"]
    results = []

    for _ in range(3):
        symbol = random.choice(symbols)
        price_change = round(random.uniform(-3, 3), 2)
        volume = round(random.uniform(100000, 1000000), 2)
        volatility = round(random.uniform(1.0, 5.0), 2)

        results.append({
            "symbol": symbol,
            "price_change_%": price_change,
            "volume": volume,
            "volatility": volatility,
            "time": datetime.now().isoformat()
        })

    return results
