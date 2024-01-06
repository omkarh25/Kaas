import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar

class PortfolioStats:
    def __init__(self, dtd_data, account_value):
        # Ensure dtd_data is a DataFrame
        if not isinstance(dtd_data, pd.DataFrame):
            raise ValueError("dtd_data must be a pandas DataFrame")
        self.dtd_data = dtd_data
        self.dtd_data['Date'] = pd.to_datetime(self.dtd_data['Date'])
        self.account_value = account_value
        
    def show_equity_curve(self):
        # Ensure 'Date' is in datetime format and sort it
        self.dtd_data['Date'] = pd.to_datetime(self.dtd_data['Date'])
        self.dtd_data.sort_values('Date', inplace=True)

        # Calculate the cumulative NetPnL to simulate the equity curve
        self.dtd_data['Cumulative NetPnL'] = self.dtd_data['NetPnL'].cumsum()
        self.dtd_data['Equity'] = self.account_value + self.dtd_data['Cumulative NetPnL']

        # Calculate the running maximum of the equity to date
        running_max = self.dtd_data['Equity'].cummax()

        # Calculate the drawdown in terms of amount and percentage
        self.dtd_data['Drawdown'] = self.dtd_data['Equity'] - running_max
        self.dtd_data['Drawdown Percent'] = (self.dtd_data['Drawdown'] / running_max) * 100

        # Plotting the Equity and Drawdown graphs
        fig, axs = plt.subplots(2, 1, figsize=(10, 8))

        # Equity Graph
        axs[0].plot(self.dtd_data['Date'], self.dtd_data['Equity'], label='Equity Curve', color='blue')
        axs[0].set_title('Equity Graph')
        axs[0].set_xlabel('Date')
        axs[0].set_ylabel('Equity')
        axs[0].grid(True)

        # Drawdown Graph
        axs[1].fill_between(self.dtd_data['Date'], 0, self.dtd_data['Drawdown Percent'], color='red', step='post')
        axs[1].set_title('Drawdown Graph')
        axs[1].set_xlabel('Date')
        axs[1].set_ylabel('Drawdown (%)')
        axs[1].grid(True)

        plt.tight_layout()  # Adjust the layout
        return fig
        
    def monthly_returns(self):
        # Ensure 'Date' is in datetime format
        self.dtd_data['Date'] = pd.to_datetime(self.dtd_data['Date'])
        
        # Accessing attributes correctly
        self.dtd_data['Month'] = self.dtd_data['Date'].dt.month_name()  # month_name is an attribute, not a method
        self.dtd_data['Year'] = self.dtd_data['Date'].dt.year  # year is an attribute, not a method

        monthly_absolute_returns = self.dtd_data.groupby(['Year', 'Month'])['NetPnL'].sum()

        # For week-on-week basis, first let's extract the week number from the Date.
        self.dtd_data['Week_Num'] = self.dtd_data['Date'].dt.isocalendar().week

        # Absolute returns for each week
        weekly_absolute_returns = self.dtd_data.groupby(['Year', 'Week_Num'])['NetPnL'].sum()

        monthly_returns_table = monthly_absolute_returns.reset_index()
        weekly_returns_table = weekly_absolute_returns.reset_index()

        # Renaming columns for clarity
        monthly_returns_table.columns = ['Year', 'Month', 'Monthly Absolute Returns (Rs.)']
        weekly_returns_table.columns = ['Year', 'Week', 'Weekly Absolute Returns (Rs.)']


        return monthly_returns_table, weekly_returns_table
    
    def max_impact_day(self):

        max_loss_day = self.dtd_data.loc[self.dtd_data['NetPnL'].idxmin()]
        max_profit_day = self.dtd_data.loc[self.dtd_data['NetPnL'].idxmax()]

        max_loss_day_date = max_loss_day['Date']
        max_loss_day_value = max_loss_day['NetPnL']

        max_profit_day_date = max_profit_day['Date']
        max_profit_day_value = max_profit_day['NetPnL']
        
        max_impact_df = pd.DataFrame({
        'Event': ['Max Loss Day', 'Max Profit Day'],
        'Date': [max_loss_day_date, max_profit_day_date],
        'NetPnL': [max_loss_day_value, max_profit_day_value]
    })

        return max_impact_df
        

    def portfolio_stats(self):
        # Recovery Factor: Net Profit / Maximum Drawdown
        net_profit = self.dtd_data['NetPnL'].sum()
        max_drawdown = -self.dtd_data['Drawdown'].min()  # Drawdown values are negative, so taking the negative of the minimum gives the maximum drawdown
        recovery_factor = net_profit / max_drawdown if max_drawdown != 0 else np.nan

        # Risk-Return Ratio: Average Annual Return / Standard Deviation of Annual Returns
        annual_return = self.dtd_data['NetPnL'].sum() / len(self.dtd_data['Year'].unique())
        annual_std = self.dtd_data.groupby('Year')['NetPnL'].sum().std()
        risk_return_ratio = annual_return / annual_std if annual_std != 0 else np.nan

        # Average Loss
        average_loss = self.dtd_data[self.dtd_data['NetPnL'] < 0]['NetPnL'].mean()

        # Compound Annual Growth Rate (CAGR)
        days = (self.dtd_data['Date'].max() - self.dtd_data['Date'].min()).days
        cagr = ((self.dtd_data['Equity'].iloc[-1] / self.account_value) ** (365/days) - 1) * 100
        
        # Win-Loss Ratio: Total Wins / Total Losses
        wins = self.dtd_data[self.dtd_data['NetPnL'] > 0]['NetPnL'].sum()
        losses = -self.dtd_data[self.dtd_data['NetPnL'] < 0]['NetPnL'].sum()  # Losses are negative, so we take the negative to make it positive
        win_loss_ratio = wins / losses if losses != 0 else np.nan

        # Sharpe Ratio: (Return of Investment - Risk Free Rate) / Standard Deviation of Returns
        # Assuming a risk-free rate of 0 for simplicity.
        daily_return = self.dtd_data['NetPnL'] / self.account_value
        sharpe_ratio = daily_return.mean() / daily_return.std() if daily_return.std() != 0 else np.nan
        
        # Calculating consecutive losses, consecutive wins, gain to pain ratio, and kelly criterion.

        # Consecutive losses and wins
        self.dtd_data['Win'] = self.dtd_data['NetPnL'] > 0
        consecutive_losses = self.dtd_data['Win'].astype(int).groupby(self.dtd_data['Win'].ne(self.dtd_data['Win'].shift()).cumsum()).cumcount()
        consecutive_wins = self.dtd_data['Win'].astype(int)[::-1].groupby(self.dtd_data['Win'].ne(self.dtd_data['Win'].shift()).cumsum()).cumcount()

        max_consecutive_losses = consecutive_losses.max()
        max_consecutive_wins = consecutive_wins.max()

        # Gain to Pain Ratio: Total Returns / Absolute Sum of All Losses
        total_returns = self.dtd_data['NetPnL'].sum()
        total_losses = -self.dtd_data[self.dtd_data['NetPnL'] < 0]['NetPnL'].sum()  # Sum of absolute losses
        gain_to_pain_ratio = total_returns / total_losses if total_losses != 0 else np.nan

        # Kelly Criterion: (Winning Probability * Average Win) / Average Loss - (Losing Probability * Average Loss) / Average Win
        # It's a formula used to determine the optimal size of a series of bets.
        winning_prob = len(self.dtd_data[self.dtd_data['NetPnL'] > 0]) / len(self.dtd_data)
        average_win =self.dtd_data[self.dtd_data['NetPnL'] > 0]['NetPnL'].mean()
        losing_prob = len(self.dtd_data[self.dtd_data['NetPnL'] < 0]) / len(self.dtd_data)
        kelly_criterion = (winning_prob * average_win / -average_loss) - (losing_prob * -average_loss / average_win) if average_loss != 0 else np.nan
        
        stats_dict = {
            'Net Profit': net_profit,
            'Max Drawdown': max_drawdown,
            'Recovery Factor': recovery_factor,
            'Risk-Return Ratio': risk_return_ratio,
            'Average Loss': average_loss,
            'CAGR': cagr,
            'Win-Loss Ratio': win_loss_ratio,
            'Sharpe Ratio': sharpe_ratio,
            'Max Consecutive Losses': max_consecutive_losses,
            'Max Consecutive Wins': max_consecutive_wins,
            'Gain to Pain Ratio': gain_to_pain_ratio,
            'Kelly Criterion': kelly_criterion
        }

        return pd.DataFrame([stats_dict])
