import pandas as pd
from Utils import Position
from Backtest import backtestN
import optuna
from typing import List
from itertools import combinations

if __name__ == '__main__':
    #optimize()
    data = pd.read_csv("/Users/edson33/Desktop/DecimoSemestre/aapl_5m_train.csv").dropna()
    data = data[:10000]

indicators_list = ['RSI', 'MACD', 'BOLL', "ADX", "SMA"]
all_combinations = []
#combo = ("RSI", "BOLL")
for i in range(1, len(indicators_list) + 1):
    all_combinations.extend(combinations(indicators_list, i))
pd.DataFrame(all_combinations)

# Backtesting for all combinations
results = {}
for combo in all_combinations:

    def optimize(trial, indicators, data):
        data = data.copy()
        sl = trial.suggest_float("sl", 0.012, 0.075)
        tp = trial.suggest_float("tp", 0.012, 0.075)
        n_shares = trial.suggest_float("n_shares", 40, 150)

        rsi_window = 0
        rsi_lower = 0
        rsi_upper = 0

        window_fast_macd = 0
        window_slo_macd = 0
        win_sig_macd = 0

        boll_wind = 0
        boll_wind_dev = 0

        if "RSI" in indicators:
            rsi_window = trial.suggest_int("rsi_window", 5, 50)
            rsi_lower = trial.suggest_float("rsi_lower", 10, 40)
            rsi_upper = trial.suggest_float("rsi_upper", 60, 90)