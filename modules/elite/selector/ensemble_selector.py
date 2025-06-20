import random
from statistics import mean
from datetime import datetime

class EnsembleStrategySelector:
    def __init__(self):
        self.history = {}

    def update_history(self, symbol, strategy_name, confidence, pnl):
        if symbol not in self.history:
            self.history[symbol] = []

        self.history[symbol].append({
            "strategy": strategy_name,
            "confidence": confidence,
            "pnl": pnl,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Spara bara de senaste 100 posterna
        if len(self.history[symbol]) > 100:
            self.history[symbol].pop(0)

    def rank_strategies(self, symbol):
        if symbol not in self.history:
            return []

        data = self.history[symbol]
        scores = {}

        for record in data:
            strat = record["strategy"]
            if strat not in scores:
                scores[strat] = {"conf": [], "pnl": []}
            scores[strat]["conf"].append(record["confidence"])
            scores[strat]["pnl"].append(record["pnl"])

        # Räkna ut en kombinerad viktning: genomsnittlig confidence * genomsnittlig PnL
        ranked = []
        for strat, values in scores.items():
            if values["conf"] and values["pnl"]:
                avg_conf = mean(values["conf"])
                avg_pnl = mean(values["pnl"])
                score = round(avg_conf * avg_pnl, 4)
                ranked.append((strat, score))

        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

    def choose_best_strategy(self, symbol):
        ranked = self.rank_strategies(symbol)
        if ranked:
            return ranked[0][0]  # Bästa strategin
        return random.choice(["BinaryMeanReversion", "ForexTrend", "CryptoSpread", "StockMomentum"])

    def print_ranking(self, symbol):
        print(f"📊 Strategiranking för {symbol}:")
        for strat, score in self.rank_strategies(symbol):
            print(f"   - {strat}: {score}")
