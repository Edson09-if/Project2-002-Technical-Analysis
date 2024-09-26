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
