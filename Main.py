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

        if "MACD" in indicators:
            window_fast_macd = trial.suggest_int("window_fast_macd", 8, 15)
            window_slo_macd = trial.suggest_int("window_slo_macd", 18, 30)
            win_sig_macd = trial.suggest_int("win_sig_macd", 5, 14)

        if "BOLL" in indicators:
            boll_wind = trial.suggest_int("boll_wind", 12, 25)
            boll_wind_dev = trial.suggest_float("boll_wind_dev", 1, 3)

        if "ADX" in indicators:
            adx_window = trial.suggest_int("adx_window", 7, 30)

        if "SMA" in indicators:
            short_sma_wind = trial.suggest_int("short_sma_wind", 5, 50)
            long_sma_wind = trial.suggest_int("long_sma_wind", 50, 200)


        final_cap = backtestN(indicators, data, sl, tp, rsi_window, rsi_lower, rsi_upper,
              boll_wind, boll_wind_dev,
             window_slo_macd, window_fast_macd, win_sig_macd, n_shares=40)
        return final_cap


    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: optimize(trial, combo, data),n_trial=3)