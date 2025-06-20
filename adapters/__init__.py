import ccxt

def get_all_balances(exchange_name: str) -> dict:
    """Returnerar en dict { 'total': <summa>, <symbol>: <balance>, … }"""
    ex_class = getattr(ccxt, exchange_name)
    ex = ex_class({'apiKey': 'DIN_KEY', 'secret': 'DITT_SECRET'})
    bal = ex.fetch_balance()
    total = sum(bal['total'].values())
    return {'total': total, **bal['total']}
