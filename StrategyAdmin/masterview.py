import plotly.graph_objects as go
import pandas as pd

# Function to create a cumulative P&L equity curve using Plotly
def plot_equity_curve(cum_df):
    # Calculate the cumulative P&L
    cum_df['cumulative_pnl'] = cum_df['net_pnl_for_date'].cumsum()

    # Create a Plotly figure
    fig = go.Figure()

    # Add a trace for the equity curve
    fig.add_trace(go.Scatter(x=cum_df['date'], y=cum_df['cumulative_pnl'],
                             mode='lines+markers',
                             name='Cumulative P&L'))

    # Customize layout
    fig.update_layout(title='Cumulative P&L Equity Curve',
                      xaxis_title='Date',
                      yaxis_title='Cumulative P&L',
                      template='plotly_white')
    
    equity_curve_fig = plot_equity_curve(cum_df)
    equity_curve_fig.show()

    return fig

# Function to create a drawdown chart using Plotly
def plot_drawdown(cum_df):
    # Calculate the drawdown
    cum_df['drawdown'] = cum_df['cumulative_pnl'] - cum_df['cumulative_pnl'].cummax()

    # Create a Plotly figure
    fig = go.Figure()

    # Add a trace for the drawdown curve
    fig.add_trace(go.Scatter(x=cum_df['date'], y=-cum_df['drawdown'],
                             fill='tozeroy',  # Fill area under the curve
                             mode='lines',
                             name='Drawdown',
                             line_color='red'))

    # Customize layout
    fig.update_layout(title='Drawdown Chart',
                      xaxis_title='Date',
                      yaxis_title='Drawdown',
                      template='plotly_white')

    return fig

def create_charts(df, column_for_calc):
    
    # Equity Chart
    df['Cumulative_PnL'] = df[column_for_calc].cumsum()
    equity_chart = go.Figure()
    equity_chart.add_trace(go.Scatter(x=df.index, y=df['Cumulative_PnL'], mode='lines', name='Equity Curve'))

    # Drawdown Chart
    roll_max = df['Cumulative_PnL'].cummax()
    drawdown = roll_max - df['Cumulative_PnL']
    drawdown_chart = go.Figure()
    drawdown_chart.add_trace(go.Scatter(x=df.index, y=drawdown, mode='lines', name='Drawdown'))

    return equity_chart, drawdown_chart


def cumulate_pnl_from_sheets(file_path, sheet_names):
    cumulative_pnl_df = pd.DataFrame()

    # Iterate through each sheet and accumulate the 'net_pnl' values
    for sheet_name in sheet_names:
        # Read the sheet data
        sheet_data = pd.read_excel(file_path, sheet_name=sheet_name)

        # Convert 'exit_time' to datetime, handling various possible formats
        sheet_data['date'] = pd.to_datetime(sheet_data['exit_time'], errors='coerce')

        # If there are any rows that couldn't be converted, drop them
        sheet_data.dropna(subset=['date'], inplace=True)

        # Normalize the date to remove the time component
        sheet_data['date'] = sheet_data['date'].dt.normalize()

        # Calculate the daily 'net_pnl'
        daily_pnl = sheet_data.groupby('date')['net_pnl'].sum().reset_index(name='net_pnl_for_date')

        # Merge with the cumulative dataframe
        if cumulative_pnl_df.empty:
            cumulative_pnl_df = daily_pnl
        else:
            cumulative_pnl_df = pd.merge(
                cumulative_pnl_df, daily_pnl,
                on='date', how='outer', suffixes=('', '_right')
            )

            # Fill NaNs with 0 and sum the 'net_pnl_for_date' columns
            cumulative_pnl_df.fillna(0, inplace=True)
            cumulative_pnl_df['net_pnl_for_date'] += cumulative_pnl_df.pop('net_pnl_for_date_right')

    # Sort the dataframe by date
    cumulative_pnl_df.sort_values('date', inplace=True)

    return cumulative_pnl_df

omkar_excel_path = r'C:\Users\user\Desktop\Kaas\StrategyAdmin\userexcel\omkar.xlsx'
sheet_names = ['AmiPy','MPWizard','ExpiryTrader','OvernightFutures','ExtraTrades','ErrorTrade']

# Example usage: Cumulate pnl from all sheets
cumulative_pnl_df = cumulate_pnl_from_sheets(omkar_excel_path, sheet_names)

# Display the head of the cumulative dataframe to verify
print(cumulative_pnl_df.head())



