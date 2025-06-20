from modules.balance_exporter import export_balances_to_csv
from deriv_status import get_deriv_balances
from binance_status import get_binance_balances
from bybit_status import get_bybit_balances
from bitget_status import get_bitget_balances

balances = {
    "Deriv": get_deriv_balances(),
    "Binance": get_binance_balances(),
    "Bybit": get_bybit_balances(),
    "Bitget": get_bitget_balances()
}
export_balances_to_csv(balances)
