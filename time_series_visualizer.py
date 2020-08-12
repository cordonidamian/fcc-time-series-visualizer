import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import calendar
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col=['date'])
df.reset_index(inplace=True)


# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    
    fig, ax = plt.subplots()
    ax.plot(df.index, df['value'] , label = 'Línea 1', linewidth = 4, color = 'red' )

    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    #df.reset_index(inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    r = df.groupby(by=[df.date.dt.year, df.date.dt.month])
    f = round(r.mean())
    f.index.names = ['year','month']
    f.reset_index(inplace=True)
    f['Months'] = f['month'].apply(lambda x: calendar.month_name[x])

    df_bar = f

    # Draw bar plot

    fig, ax = plt.subplots()
    g = sns.catplot(x="year", y="value", hue="Months", data=df_bar, height=6, kind="bar", palette="bright", legend=False,)
    g.despine(left=True)
    g.set_ylabels("Average Page Views")
    g.set_xlabels("Years")
    plt.legend(title='Months', loc='upper left', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    fig = g.fig

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    #df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2)

    ax1 = sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
    ax2 = sns.boxplot(x="month", y="value", data=df_box, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ax=ax[1])

    ax1.set(xlabel="Year", ylabel = "Page Views")
    ax2.set(xlabel="Month", ylabel = "Page Views")
    
    ax1.set(title='Year-wise Box Plot (Trend)')
    ax2.set(title='Month-wise Box Plot (Seasonality)')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
