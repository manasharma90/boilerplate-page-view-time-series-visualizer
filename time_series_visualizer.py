import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col=['date'])

# Clean data
mask_views = (df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))
df = df[mask_views]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize = (18,6))
    plt.plot(df.index, df['value'])
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Create new figure
    # Copy and modify data for monthly bar plot
    df_bar = df.reset_index()

    #splitting date, month, year columns
    df_bar['day'] = df_bar['date'].dt.day
    df_bar['month'] = df_bar['date'].dt.month
    df_bar['year'] = df_bar['date'].dt.year

    #keeping only relevant columns for bar plot

    df_bar = df_bar[['year', 'month', 'value']]

    #creating pivot table for final plot
    df_bar = df_bar.pivot_table(index= 'year', columns= 'month', values= 'value', aggfunc= np.mean)

    month_names = ['January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August', 'September', 
            'October', 'November', 'December']
   
    df_bar.columns = month_names

    # Draw bar plot
    axes = df_bar.plot(kind = 'bar', figsize = (10, 6))
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title = 'Months', prop={'size': 7})
    fig = axes.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    #create a grid for the two plots
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    #plot the first graph
    sns.boxplot(data = df_box, ax = axes[0], x = 'year', y = 'value').set(xlabel = 'Year', ylabel = 'Page Views', title=  "Year-wise Box Plot (Trend)")

    #create an ordered list of months for the second graph
    month_order = ['Jan', 'Feb', 'Mar', 'Apr',
            'May', 'Jun', 'Jul', 'Aug', 'Sep', 
            'Oct', 'Nov', 'Dec']

    #plot the second graph
    sns.boxplot(data = df_box, ax = axes[1], x = 'month', y = 'value', order = month_order).set(xlabel = 'Month', ylabel = 'Page Views', title=   "Month-wise Box Plot (Seasonality)")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
