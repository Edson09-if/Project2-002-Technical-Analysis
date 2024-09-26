import ta
import pandas as pd
import numpy as np
import optuna
from typing import List
from itertools import combinations
#from matplotlib import pyplot as plt

data = pd.read_csv("/Users/edson33/Desktop/DecimoSemestre/aapl_5m_train.csv").dropna()
data = data[:10000]

def backtestN(indicators: list, data: pd.DataFrame, sl: float, tp: float,
              rsi_window: int = 0, rsi_lower: int = 0, rsi_upper: int = 0,
              boll_wind: int = 0, boll_wind_dev :int = 0,
              window_slo_macd :int = 0, window_fast_macd :int = 0, win_sig_macd :int = 0,
              adx_window :int = 1 ,short_sma_wind:int =0, long_sma_wind :int =0,
              n_shares=40) -> float:
    data = data.copy()

    capital = 1_000_000
    active_positions = []
    COM = .25 / 100

    # Calculate indicators
    if 'RSI' in indicators:
        # RSI
        rsi = ta.momentum.RSIIndicator(data.Close, window=rsi_window)
        data["rsi"] = rsi.rsi()

    if 'BOLL' in indicators:
        # Boll
        bollinger = ta.volatility.BollingerBands(close=data.Close,
                                                 window=boll_wind,
                                                 window_dev=boll_wind_dev)

        data["BollingerL"] = bollinger.bollinger_lband_indicator() # unica señal de trading
        data["BollingerH"] = bollinger.bollinger_hband_indicator() # unica señal de trading

    if "MACD" in indicators:
        macd_indicator = ta.trend.MACD(close=data['Close'], window_slow=window_slo_macd,
                                       window_fast=window_fast_macd, window_sign=win_sig_macd)

        # Añadir las columnas MACD y línea de señal al DataFrame
        data['MACD'] = macd_indicator.macd()
        data['MACD_signal'] = macd_indicator.macd_signal()

    if "ADX" in indicators:
        adx_indicator = ta.trend.ADXIndicator(high=data.High, low=data.Low,
                                              close=data.Close, window=adx_window)

        data['ADX'] = adx_indicator.adx()
        data['ADX_pos'] = adx_indicator.adx_pos()
        data['ADX_neg'] = adx_indicator.adx_neg()

    if "SMA" in indicators:
        short_sma = ta.trend.SMAIndicator(data.Close ,window=short_sma_wind)
        long_sma = ta.trend.SMAIndicator(data.Close ,window=long_sma_wind)

        data["short_sma"] = short_sma.sma_indicator()
        data["long_sma"] = long_sma.sma_indicator()



    print(indicators)

    active_positions = []
    short_positions = []
    portfolio_value = [capital]
    initial_margin = 1.28
    maintenance_margin = 1.25
    equity = capital
    margin_calls = []
    margin_acc = 0


    for i, row in data.iterrows():

        long_signals = []
        short_signals = []

        for indicator in indicators:
            if 'RSI' in indicators:
                long_signals.append(row.rsi < rsi_lower)
                short_signals.append(row.rsi > rsi_upper)
            if 'BOLL' in indicators:
                long_signals.append(row.BollingerL)
                short_signals.append(row.BollingerH)
            if "MACD" in indicators:
                long_signals.append(row.MACD > row.MACD_signal)
                short_signals.append(row.MACD < row.MACD_signal)

            if "ADX" in indicators:
                long_signals.append(row.ADX_pos > row.ADX_neg and row.ADX > 25)
                short_signals.append(row.ADX_neg > row.ADX_pos and row.ADX > 25)

            if "SMA" in indicators:
                long_signals.append(row.long_sma > row.short_sma)
                short_signals.append(row.long_sma < row.short_sma)


        trading_signal = sum(long_signals) == len(long_signals)
        trading_signal_short = sum(short_signals) == len(short_signals)

        # Closing Long Position
        for position in active_positions.copy():
            if row.Close > position.price * (1 + tp):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)
            if row.Close < position.price * (1 - sl):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)

        # Open long positions
        if trading_signal:
            if capital > row.Close * n_shares * (1 + COM):
                capital -= row.Close * n_shares * (1 + COM)
                active_positions.append \
                    (Position(ticker="AAPL", price=row.Close,  n_shares = n_shares, timestamp = row.Timestamp))

        # Open short positions
        if trading_signal_short:
            short_sell = row.Close * n_shares
            required_margin = short_sell * initial_margin
            if capital >= required_margin:
                capital -= short_sell * (COM) + required_margin
                margin_acc += required_margin
                short_positions.append \
                    (Position(ticker="AAPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

        # Portfolio value
        long = sum \
            ([position.n_shares * row.Close for position in active_positions]) # Long value is based on last close price
        short = sum([position.n_shares * (position.price - row.Close) for position in short_positions])  # Short value is based on initial sell price
        short_margin = sum([position.n_shares * row.Close for position in short_positions])  # Short value is based on initial sell price
        equity = capital + long - short
        portfolio_value.append(equity)

    # Backtesting is done :
    for position in active_positions.copy():
        capital += row.Close * position.n_shares * (1 - COM)
        active_positions.remove(position)

    for position in short_positions.copy():
        capital += row.Close * position.n_shares * (1 - COM)
        short_positions.remove(position)

    # Ratio de Sharp
    risk_free_rate =0.04
    returns = np.diff(portfolio_value) / portfolio_value[:-1]
    excess_returns = returns - risk_free_rate / 252  # Ajustar por el número de días de trading
    sharp_ratio = np.mean(excess_returns) / np.std(excess_returns)

    # maxdrawdown
    peak = np.maximum.accumulate(portfolio_value)
    drawdown = (peak - portfolio_value) / peak
    max_drawdown = np.max(drawdown)

    print("Port Value:" ,portfolio_value[-1])
    print("Max_Draw:" ,max_drawdown)
    print("Sharp:" ,sharp_ratio)


    # return portfolio_value #Para graficar
    # return portfolio_value[-1]
    return sharp_ratio
    # return max_drawdown