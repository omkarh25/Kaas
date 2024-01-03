import pandas as pd
import plotly.express as px
import streamlit as st

def generate_interactive_calendar_heatmap(df, date_column, value_column):
    # Load the data from the 'AmiPy' sheet

    # Ensure the date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Prepare the data for the heatmap
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['day'] = df[date_column].dt.day
    df['day_of_week'] = df[date_column].dt.dayofweek  # 0 is Monday

    # Custom color scale for negative (red) and positive (green) values
    color_scale = [[0, "red"], [0.5, "white"], [1, "green"]]

    # Creating the interactive heatmap
    fig = px.density_heatmap(df, x="day_of_week", y="day", z=value_column, 
                             facet_col="month", facet_row="year", 
                             color_continuous_scale=color_scale,
                             title="Interactive Calendar Heatmap")

    return fig