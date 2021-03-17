import numpy as np
import dataframeTool
import displayTool
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import matplotlib as mpl
from matplotlib import style
import pandas as pd
import seaborn as sns
#sns.set(style='ticks', palette='RdBu')
sns.set()  # use Seaborn styles
from pivottablejs import pivot_ui
pd.options.display.max_colwidth = 1000
pd.options.display.max_rows = 100

# ------------------------- FUNCTION NOT USED (BEGIN) --------------------------------

# https://stackoverflow.com/questions/53811565/plotting-pandas-dataframe-from-pivot-table
# https://github.com/nicolaskruchten/jupyter_pivottablejs
def displayPivotTable():
    df = pd.DataFrame({
      'State': np.repeat(['Alaska', 'Maine', 'Michigan', 'Minnesota','Wisconsin'], 3),
      'Year': [1960, 1961, 1962]*5,
      'Murder Rate': [10.2, 11.5, 4.5, 1.7, 1.6, 1.4, 4.5, 4.1, 3.4, 1.2, 1.0, .9, 1.3, 1.6, .9]})

    pivot_ui(df, outfile_path="yourpathname.html")

# ------------------------- FUNCTION NOT USED (END) --------------------------------  

def top_10_countries_years(df):
    displayTool.printmd("**10 Top Countries / Years**",  color="blue")
    ten=dataframeTool.top_ten_countries(df)
    #fig = plt.figure(figsize=(6, 6))
    fig = plt.figure(figsize=(20, 15))
    #fig.subplots(figsize=(12, 8))
    fig.subplots_adjust(hspace=1, wspace=1)
    i=1
    for x in np.nditer(ten):
        #print(x, end=' ')
        countries_years(df,str(x),i, fig)
        i=i+1;     
                       
def countries_years(df,country_name, i, fig):
    ax1 = fig.add_subplot(5, 2, i)    
    print("Country: " + country_name)
    df = df.loc[df['country'] == country_name]
    # df1 = df.groupby(['country','year']).size().unstack().plot(kind='bar',stacked=True).plot(kind='bar',stacked=True)
    #fig = plt.figure(figsize=(20,15))
    #ax1 = fig.add_subplot(223)
    grouped_data = df.groupby(['country', 'year']).agg({'price':sum}).reset_index().sort_values(by="country", ascending=False)
    pal = sns.color_palette("Greens_d", len(grouped_data))
    sns.set_palette(pal)
    sns.barplot(x="country", y="price", hue="year", data=grouped_data, ax=ax1)
    plt.show()

def top_10_countries_months(df):
    displayTool.printmd("**10 Top Countries / Months**",  color="blue")
    ten=dataframeTool.top_ten_countries(df)
    fig = plt.figure(figsize=(30, 15))
    fig.subplots_adjust(hspace=1, wspace=1)
    i=1
    for x in np.nditer(ten):
        #print(x, end=' ')
        countries_months(df,str(x),i,fig)
        i=i+1;         

def countries_months(df,country_name, i, fig):
    #ten=dataframeTool.top_ten_countries(df)
    #df1 = df.loc[df['country'].isin(ten)]
    ax1 = fig.add_subplot(10, 1, i)    
    print("Country: " + country_name)
    df = df.loc[df['country'] == country_name]
    df.pivot_table('price', index=["month"], columns=["year","country"], aggfunc='sum').plot()
    plt.ylabel('price per month');
    plt.show()
    
def all_countries_year_months(df):
    # https://jakevdp.github.io/PythonDataScienceHandbook/03.09-pivot-tables.html
    displayTool.printmd("**All Countries / Years / Months**",  color="blue")
    df.pivot_table('price', index=["month"], columns=["year"], aggfunc='sum').plot()
    plt.ylabel('price per month for all countries');
    plt.show()
    
def all_countries_days_of_week(df):
    displayTool.printmd("**All Countries / Days of Week**",  color="blue")
    df.index = pd.to_datetime(10000 * df.year + 100 * df.month + df.day, format='%Y%m%d')
    df['dayofweek'] = df.index.dayofweek
    df.pivot_table('price', index='dayofweek', columns='year', aggfunc='mean').plot()
    plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
    plt.ylabel('mean price by day');
    plt.show()    
        
def plot_corr(df):
    f, ax = plt.subplots(figsize=(12, 8))
    corrMatrix = df.corr()
    sns.heatmap(corrMatrix, annot=True)
    corrMatrix.style.background_gradient(cmap='coolwarm').set_precision(2)
    plt.show()

def plot_graphs_df(df):
    displayTool.printmd("** Number of Invoices per day of Week**",  color="blue")
    df['day_of_week'] = df['invoice_date'].dt.day_name()
    sns.countplot(x='day_of_week', data=df)
    plt.xticks(rotation=90) 
    # if plt.show() is not used then the graph can appear after other instructions in the code...
    # https://stackoverflow.com/questions/458209/is-there-a-way-to-detach-matplotlib-plots-so-that-the-computation-can-continue
    plt.show() 
    displayTool.printmd("** Number of Invoices per Month over the years**",  color="blue")
    df['Journey_Month'] = pd.to_datetime(df.invoice_date, format='%d/%m/%Y').dt.month_name()
    sns.countplot(x='Journey_Month', data=df)
    plt.xticks(rotation=90)     
    plt.show() 
    #There is no time information for invoice_date - so the following can not retrieve anything
    #displayTool.printmd("** Number of Invoices per Night [0-6}, Morning [6-12], Afternoon [12-18] and Evening[18-24]**",  color="blue")
    #df['invoice_date_t'] = pd.to_datetime(df.invoice_date, format='%H:%M')
    #a = df.assign(invoice_date_session=pd.cut(df.invoice_date_t.dt.hour,[0,6,12,18,24],labels=['Night','Morning','Afternoon','Evening']))
    #df['invoice_date_S'] = a['invoice_date_session']
    #sns.countplot(x='invoice_date_S', data=df)
    #plt.xticks(rotation=90)     
    #plt.show()
       
def plot_ts_df(df):
    df['day_of_week'] = df['date'].dt.day_name()
    sns.countplot(x='day_of_week', data=df)
    plt.xticks(rotation=90)
    plt.show()    
    sns.countplot(x='year_month', data=df)
    plt.xticks(rotation=90)  
    plt.show()    
    
def plot_ts_df_2(df):
    #https://unidata.github.io/python-training/workshop/Time_Series/basic-time-series-plotting/
    fig, ax = plt.subplots(figsize=(10, 6))
    # Specify how our lines should look
    ax.plot(df.date, df.revenue, color='tab:orange', label='Revenue')
    # Same as above
    ax.set_xlabel('Date')
    ax.set_ylabel('Revenue')
    ax.set_title('Capstone Data')
    ax.grid(True)  
    ax.legend(loc='upper left');
    plt.show()
   
def plot_ts_df_3(df):
    #https://unidata.github.io/python-training/workshop/Time_Series/basic-time-series-plotting/
    fig, ax = plt.subplots(figsize=(10, 6))
    axb = ax.twinx()   
    ax.set_xlabel('Date')
    ax.set_ylabel('Revenue')
    ax.set_title('Capstone Time series Data')
    ax.grid(True)
    # Plotting on the first y-axis
    ax.plot(df.date, df.revenue, color='tab:orange', label='Revenue')
    #ax.plot(df.time, df.wind_gust, color='tab:olive', linestyle='--', label='Wind Gust')
    # Plotting on the second y-axis
    axb.set_ylabel('Purchases')
    axb.plot(df.date, df.purchases, color='black', label='Purchases')

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

    # Handling of getting lines and labels from all axes for a single legend
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = axb.get_legend_handles_labels()
    axb.legend(lines + lines2, labels + labels2, loc='upper left');
    plt.show()
   
   