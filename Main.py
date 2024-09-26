import pandas as pd
from Utils import optimize
from Backtest import BacktestN
import optuna

if _name_ == '_main_':
    #optimize()
    data = pd.read_csv("aapl_5m_train.csv").dropna()
    data = data[:5000]

indicators_list = ['RSI', 'MACD', 'BOLL', "ADX", "SMA"]
all_combinations = []
#combo = ("RSI", "BOLL")
for i in range(1, len(indicators_list) + 1):
    all_combinations.extend(combinations(indicators_list, i))
pd.DataFrame(all_combinations)