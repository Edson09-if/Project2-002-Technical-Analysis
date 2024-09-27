import pandas as pd
import matplotlib.pyplot as plt

def plot_portfolio_value(portfolio_value, data: pd.DataFrame):
    initial_investment = 1_000_000
    data = data.copy()
    initial_price = data['Close'].iloc[0]
    shares_bought = initial_investment / initial_price
    data['Portfolio_Value_Pasive'] = shares_bought * data['Close']

    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value, label='Optimize Portfolio Value')
    plt.plot(data['Portfolio_Value_Pasive'], label='Pasive Portfolio Value')
    plt.title('Portfolio Value')
    plt.xlabel('Days')
    plt.ylabel('USD')
    plt.legend()
    plt.show()
    plt.grid()

class Position:
    def __init__(self, ticker:str, price:float, n_shares: int, timestamp:float):
        self.ticker = ticker
        self.price =price
        self.n_shares = n_shares
        self.timestamp = timestamp

class Metrcis:
    def sharperatio(portfolio_value, risk_free_rate=0.04):
        # Calcular los retornos
        returns = np.diff(portfolio_value) / portfolio_value[:-1]
        excess_returns = returns - risk_free_rate / 252  # Ajustar por el número de días de trading
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
        return sharpe_ratio

    def maxdrawdown(portfolio_value):
        peak = np.maximum.accumulate(portfolio_value)
        drawdown = (peak - portfolio_value) / peak
        max_drawdown = np.max(drawdown)
        return max_drawdown

    def winlossratio(trades):
        wins = sum(1 for trade in trades if trade > 0)
        losses = sum(1 for trade in trades if trade < 0)
        return wins / (wins + losses) if (wins + losses) > 0 else 0

## PLOT FUNCTIONS
class Plots:
    def plot_sharperatio(sharpe_ratio):
        plt.figure(figsize=(6, 4))
        plt.bar(['Sharpe Ratio'], [sharpe_ratio], color='blue')
        plt.title('Sharpe Ratio')
        plt.ylabel('Value')
        plt.grid(axis='y')
        plt.show()


    def plot_winlossratio(win_loss_ratio):
        plt.figure(figsize=(6, 4))
        plt.bar(['Win', 'Loss'], [win_loss_ratio, 1 - win_loss_ratio], color=['green', 'red'])
        plt.title('Win-Loss Relation')
        plt.ylabel('Porportion')
        plt.grid(axis='y')
        plt.show()


    def plot_maxdrawdown(portfolio_value):
        peak = np.maximum.accumulate(portfolio_value)
        drawdown = (peak - portfolio_value) / peak

        plt.figure(figsize=(12, 6))
        plt.fill_between(range(len(drawdown)), drawdown, color='red', alpha=0.5)
        plt.title('Max Drawdown')
        plt.xlabel('Days')
        plt.ylabel('Drawdown (%)')
        plt.grid()
        plt.show()

