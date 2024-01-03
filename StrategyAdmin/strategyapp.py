# Required imports
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import stats as stats
import os
import glob
import calendarview
import masterview

def display_formatted_statistics(formatted_stats):
    # Convert the statistics to a DataFrame for better display
    stats_df = pd.DataFrame(list(formatted_stats.items()), columns=['Metric', 'Value'])

    # Apply conditional formatting
    def color_value(val):
        color = 'black'  # default
        try:
            num = float(val)
            if num < 0:
                color = 'red'  # bad
            elif num > 0:
                color = 'green'  # good
            # Add more conditions for 'okay' or other statuses
        except ValueError:
            pass  # Keep default color for non-numeric values
        return f'color: {color};'
    st.write(stats_df.style.applymap(color_value))
    
##################################################################
    
# Function to get all excel files in the specified folder
def get_excel_files(folder_path):
   pattern = f"{folder_path}/*.xlsx"
   return glob.glob(pattern)

# Function to get all sheet names (strategies) from an Excel file
def get_sheet_names(file_path):
    xl = pd.ExcelFile(file_path)
    return xl.sheet_names

# Function to process the selected sheet and return data, stats, and charts
def process_sheet(file_path, sheet_name):
    # Attempt to load the specific sheet from the excel file
    try:
        # Check if the sheet_name exists in the file
        xl = pd.ExcelFile(file_path)
        if sheet_name in xl.sheet_names:
            data = pd.read_excel(file_path, sheet_name=sheet_name)
            data['exit_time'] = pd.to_datetime(data['exit_time'])
            return data
        else:
            print(f"Sheet '{sheet_name}' does not exist in the file.")
            return None  # or handle it as you see fit

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None  # or handle as needed
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        return None  # or handle as needed

def determine_file_type(file_name):
    # Implement your logic here. For example, you might check the file name pattern
    if "signals" in file_name.lower():
        return "signals"
    else:
        return "user"

# Streamlit app
def main():
    st.title("Trading Strategy Analyzer")

    # Define path of folder containing excel files
    folder_path = r'C:\Users\user\Desktop\Kaas\StrategyAdmin\userexcel'  # Update this with the actual folder path

    # Get all excel files in the folder
    excel_files = get_excel_files(folder_path)

    # Sidebar for file selection
    selected_file = st.sidebar.radio("Choose a file", excel_files)

    # Get sheet names (strategies) from the selected file
    sheet_names = get_sheet_names(os.path.join(folder_path, selected_file))
    print("sheet_names",sheet_names)

    # Sidebar for strategy selection
    selected_strategy = st.sidebar.radio("Choose a strategy", sheet_names)
    print("selected_strategy",selected_strategy)

    # Determine whether the selected file is 'Signals' or a user file
    is_signals = 'Signals' in selected_file

    # Process the selected sheet and get data, stats, and charts
    data = process_sheet(os.path.join(folder_path, selected_file), selected_strategy)
    print("data",data)

    # Create tabs for 'Data', 'Stats', and 'Charts'
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data", "Stats", "Charts","Calendar","MasterView"])

    with tab1:
        st.write("Data")
        st.write(f"Data for {selected_strategy}", data)

    with tab2:
        st.header('Trading Statistics')
        # Assuming a function calculate_all_stats(df) that returns a DataFrame of all stats
        formatted_stats = stats.return_statistics(data,is_signals)
        display_formatted_statistics(formatted_stats)

    with tab3:
        st.header('Performance Charts')
        column_for_calc = 'trade_points' if is_signals else 'net_pnl'
        equity_chart, drawdown_chart = masterview.create_charts(data,column_for_calc)  # This should return a plotly.graph_objs.Figure
        # Use the figure directly in st.plotly_chart
        st.header('Equity Curve')
        st.plotly_chart(equity_chart, use_container_width=True)
        st.divider()
        st.header('Drawdown Curve')
        st.plotly_chart(drawdown_chart, use_container_width=True)
        
    with tab4:
        st.header('Calendar View')
        column_for_calc = 'trade_points' if is_signals else 'net_pnl'

        fig1 =calendarview.generate_interactive_calendar_heatmap(data, 'exit_time', column_for_calc)
        # Display the plot in Streamlit
        st.plotly_chart(fig1)
        
    with tab4:
        st.header('Master View')
        # column_for_calc = 'net_pnl_for_date'
        # file_path = os.path.join(folder_path, selected_file)
        # sheet_names = ['AmiPy','MPWizard','ExpiryTrader','OvernightFutures','ExtraTrades','ErrorTrade']
        # cum_df = masterview.cumulate_pnl_from_sheets(file_path, sheet_names)
        # print("cum_df",cum_df)
        # equity_chart_1 = masterview.plot_equity_curve(cum_df)  # This should return a plotly.graph_objs.Figure
        # drawdown_chart_1 = masterview.plot_drawdown(cum_df)  # This should return a plotly.graph_objs.Figure
        # # # Use the figure directly in st.plotly_chart
        # st.header('Equity Curve')
        # st.plotly_chart(equity_chart_1, use_container_width=True)
        # st.divider()
        # st.header('Drawdown Curve')
        # st.plotly_chart(drawdown_chart_1, use_container_width=True)
        

# Run the app
if __name__ == '__main__':
    main()
