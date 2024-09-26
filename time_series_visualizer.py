import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from calendar import month_name
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#Obrigado https://stackoverflow.com/questions/60624571/sort-list-of-month-name-strings-in-ascending-order
month_lookup = list(month_name)

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv').set_index('date')

# Clean data
df.dropna(inplace=True)
df = df[(df['value'] < df['value'].quantile(0.975)) & (df['value'] > df['value'].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(12,6))
    plt.plot(df.index, df.value)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')



    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df
    df_bar.index = pd.to_datetime(df_bar.index)
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_name[1:], ordered=True)
    monthAvg = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    # Draw bar plot
    fig = plt.figure(figsize=(12,6))
    monthAvg.plot(kind="bar", ax=plt.gca())
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.title('Monthly Average Page Views by Year')
    plt.legend(title="Months", loc='upper left')


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    #Não sei o que fazer aqui... O código já pronto está dando problema
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    fig, axes = plt.subplots(1,2, figsize=(12,6))
    # Draw box plots (using Seaborn)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
