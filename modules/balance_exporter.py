import csv
import os
from datetime import datetime

EXPORT_PATH = os.path.expanduser("~/NikolaDeploy/data/balance_export.csv")

def export_balances_to_csv(balances: dict):
    try:
        with open(EXPORT_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Plattform", "Konto", "Valuta", "Saldo", "Typ", "Tid"])

            timestamp = datetime.utcnow().isoformat()
            for platform, data in balances.items():
                writer.writerow([
                    platform,
                    data.get("loginid", "N/A"),
                    data.get("currency", "N/A"),
                    data.get("balance", 0),
                    "Demo" if data.get("is_virtual", False) else "Live",
                    timestamp
                ])
        print(f"✅ Balans exporterad till CSV: {EXPORT_PATH}")
    except Exception as e:
        print(f"❌ Exportfel: {e}")
