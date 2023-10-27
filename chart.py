import datetime
import pandas
import matplotlib.pyplot as plt
import numpy as np

def create_high_avg_chart(df: pandas.DataFrame, df_new: pandas.DataFrame): 
    df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    old_years_data = df.groupby(df['Date'].dt.year)
    old_high_avg = {}
    for year, group in old_years_data:
        old_high_avg[year] = group['High'].mean()
    
    df_new['Date'] = df_new['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    new_years_data = df_new.groupby(df_new['Date'].dt.year)
    new_high_avg = {}
    for year, group in new_years_data:
        new_high_avg[year] = group['High'].mean()

    years = old_high_avg.keys()
    chart_data = {
        'Avg High Old': tuple(old_high_avg.values()),
        'Avg High New': tuple(new_high_avg.values())
    }

    x = np.arange(len(years))  # the label locations
    width = 0.5  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in chart_data.items():
        offset = width * multiplier + 0.25
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, fmt='%.0f')
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('USD')
    ax.set_title('Среднее значение максимума')
    ax.set_xticks(x + width, years)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 400)
    fig.set_size_inches(19, 9)

    return fig

def create_low_avg_chart(df: pandas.DataFrame, df_new: pandas.DataFrame): 
    df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    old_years_data = df.groupby(df['Date'].dt.year)
    old_low_avg = {}
    for year, group in old_years_data:
        old_low_avg[year] = group['Low'].mean()
    
    df_new['Date'] = df_new['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    new_years_data = df_new.groupby(df_new['Date'].dt.year)
    new_low_avg = {}
    for year, group in new_years_data:
        new_low_avg[year] = group['Low'].mean()

    years = old_low_avg.keys()
    chart_data = {
        'Avg Low Old': tuple(old_low_avg.values()),
        'Avg Low New': tuple(new_low_avg.values())
    }

    x = np.arange(len(years))  # the label locations
    width = 0.5  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in chart_data.items():
        offset = width * multiplier + 0.25
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, fmt='%.0f')
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('USD')
    ax.set_title('Среднее значение минимума')
    ax.set_xticks(x + width, years)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 400)
    fig.set_size_inches(19, 9)

    return fig


    
    