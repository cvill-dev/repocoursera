import pandas as pd
import numpy as np
import re
import os
import datetime
from timeit import default_timer as timer
import multiprocessing
import displayTool
from collections import defaultdict

def renameColumn(df):
    correct_columns = ['country', 'customer_id', 'day', 'invoice', 'month',
                       'price', 'stream_id', 'times_viewed', 'year']
    cols = set(df.columns.tolist())
    if 'StreamID' in cols:
            df.rename(columns={'StreamID':'stream_id'},inplace=True)
    if 'TimesViewed' in cols:
            df.rename(columns={'TimesViewed':'times_viewed'},inplace=True)
    if 'total_price' in cols:
            df.rename(columns={'total_price':'price'},inplace=True)

    cols = df.columns.tolist()
    if sorted(cols) != correct_columns:
            raise Exception("columns name could not be matched to correct cols")

    return df

# addColumn function = 3 secondes
def addColumn(df):
    years,months,days = df['year'].values,df['month'].values,df['day'].values 
    dates = ["{}-{}-{}".format(years[i],str(months[i]).zfill(2),str(days[i]).zfill(2)) for i in range(df.shape[0])]
    df['invoice_date'] = np.array(dates,dtype='datetime64[D]')
    df['invoice'] = [re.sub("\D+","",i) for i in df['invoice'].values]
    ## sort by date and reset the index
    df.sort_values(by='invoice_date',inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

def displayUniqueValues(df):
    countries = np.unique(df['country'].values)
    countries_number = np.unique(df['country'].values).size
    displayTool.printmd("**Countries Info:**",  color="blue")
    for c in countries:
        print(c, end = ' ')
    print("\nNumber of different countries: " + str(countries_number))
    displayTool.printmd("**Top Ten countries in term of revenue:**",  color="blue")
    ten = top_ten_countries(df)
    print(ten)
    #streams = np.unique(df['stream_id'].values)
    streams_number = np.unique(df['stream_id'].values).size
    displayTool.printmd("**Streams Info:**",  color="blue")
    #print("The list of the streams is : ")
    #for s in streams:
    #    print(s, end = ' ')
    print("\nNumber of different streams: " + str(streams_number))    
    years = np.unique(df['year'].values)
    years_number = np.unique(df['year'].values).size    
    displayTool.printmd("**Years Info:**",  color="blue")
    for y in years:
        print(y, end = ' ')
    print("\nNumber of different years: " + str(years_number))


def displayPivotTables(df):    
    # A single index
    # Using pandas.DataFrame.pivot_table
    displayTool.printmd("**Pivot Table Index(country), Values(price)**",  color="blue")
    table1 = pd.pivot_table(df,index='country',values="price",aggfunc='sum')
    print(table1)
    #table1.plot(figsize=(30, 10))
    
    displayTool.printmd("**Pivot Table Index(country), Values(price), Columns(year)**",  color="blue")
    table2 = pd.pivot_table(df,index=["country"],values=["price"], columns=["year"], aggfunc='sum',fill_value=0)
    print(table2)
     
    displayTool.printmd("**Pivot Table Index(country, year), Values(price, times_viewed)**",  color="blue")
    # Sum aggregate function is applied to both the values
    table3 = pd.pivot_table(df,index=["country","year"],values=["price","times_viewed"], aggfunc='sum')
    print(table3)

    displayTool.printmd("**Pivot Table Index(country, year), Values(price), Columns(stream_id)**",  color="blue")
    table4 = pd.pivot_table(df,index=["country","year"],values=["price"], columns=["stream_id"], aggfunc=[np.sum],fill_value=0)
    print(table4)   
   
    displayTool.printmd("**Pivot Table Index(country, year, stream_id), Values(price, times_viewed)**",  color="blue")
    # Multiple indexes
    table5 = pd.pivot_table(df,index=["country","year","stream_id"],values=["price", "times_viewed"], aggfunc='sum')  
    print(table5)
   
    displayTool.printmd("**Pivot Table Index(country, year, stream_id), Values(price, times_viewed)**",  color="blue")
    table6 = pd.pivot_table(df,index=["country","year","stream_id"],values=["price", "times_viewed"], aggfunc=[np.sum,np.mean],fill_value=0,margins=True)
    print(table6)


def display_df_info(df):
    print('\n')
    displayTool.printmd("**df.info:**",  color="blue")
    print(df.info())
    print("\n\tdf: {} x {}".format(df.shape[0], df.shape[1]))
    print('\n')
    displayTool.printmd("**Missing values:**",  color="blue")
    print("\tMissing Value Summary\n{}".format("-"*35))
    print(df.isnull().sum(axis = 0))
    print('\n')
    displayTool.printmd("**df.describe:**",  color="blue")
    print(df.describe())
    print('\n')
    displayTool.printmd("**df.head:**",  color="blue")
    print(df.head())
    displayUniqueValues(df)
    displayTool.printmd("**df year value counts:**",  color="blue")
    vc=df['year'].value_counts()
    print(vc)
    displayTool.printmd("**df year month price sum:**",  color="blue")
    v2 = df.groupby(['year', 'month'])['price'].sum()
    print(v2)
    displayTool.printmd("**df year month price max:**",  color="blue")
    v3 = df.groupby(['year', 'month']).agg({'price':max})
    print(v3)
    displayTool.printmd("**How many days did the entire range of dates span?**",  color="blue")
    v4= df.invoice_date.nunique()
    print(v4)
    displayTool.printmd("**How many different countries?**",  color="blue")
    v5= df.country.nunique()
    print(v5)
    displayTool.printmd("**How many invoices per country?**",  color="blue")
    v6= df.country.value_counts()
    print(v6)
   
    
def top_ten_countries(df):
    ## find the top ten countries (wrt revenue)
    table = pd.pivot_table(df,index='country',values="price",aggfunc='sum')
    table.columns = ['total_revenue']
    table.sort_values(by='total_revenue',inplace=True,ascending=False)
    top_ten_countries =  np.array(list(table.index))[:10]
    return top_ten_countries

def transform(df):
    start = timer()
    df1=addColumn(df)
    end = timer()
    duration = end - start
    print("\tDuration for the dataframe transformation: " + str(duration))
    return df1
    
def display_ts_df_info(df):
    displayTool.printmd("**ts df.head:**",  color="blue")
    print(df.head())
    displayTool.printmd("**ts df.info:**",  color="blue")
    print(df.info())
    displayTool.printmd("**ts df.count:**",  color="blue")
    print(df.count())
    displayTool.printmd("**ts df.count where pourchases = 0 :**",  color="blue")
    print(len(df[df['purchases'] == 0]))
  
    
def convert_to_ts(df_orig, country=None):
    """
    given the original DataFrame (fetch_data())
    return a numerically indexed time-series DataFrame 
    by aggregating over each day
    """
    start = timer()
    if country:
        if country not in np.unique(df_orig['country'].values):
            raise Excpetion("country not found")
    
        mask = df_orig['country'] == country
        df = df_orig[mask]
    else:
        df = df_orig
        
    ## use a date range to ensure all days are accounted for in the data
    invoice_dates = df['invoice_date'].values
    #print(invoice_dates)
    start_month = '{}-{}'.format(df['year'].values[0],str(df['month'].values[0]).zfill(2))
    stop_month = '{}-{}'.format(df['year'].values[-1],str(df['month'].values[-1]).zfill(2))
    df_dates = df['invoice_date'].values.astype('datetime64[D]')
    days = np.arange(start_month,stop_month,dtype='datetime64[D]')
    
    purchases = np.array([np.where(df_dates==day)[0].size for day in days])
    invoices = [np.unique(df[df_dates==day]['invoice'].values).size for day in days]
    streams = [np.unique(df[df_dates==day]['stream_id'].values).size for day in days]
    views =  [df[df_dates==day]['times_viewed'].values.sum() for day in days]
    revenue = [df[df_dates==day]['price'].values.sum() for day in days]
    year_month = ["-".join(re.split("-",str(day))[:2]) for day in days]

    df_time = pd.DataFrame({'date':days,
                            'purchases':purchases,
                            'unique_invoices':invoices,
                            'unique_streams':streams,
                            'total_views':views,
                            'year_month':year_month,
                            'revenue':revenue}) 
    end = timer()
    duration = end - start
    print("\tDuration for the transformation to an indexed Dataframe: " + str(duration))  
    return(df_time)
  
def fetch_ts(df,df1):
    ts_data_dir = os.path.join(".","ts-data")
    
    ## if files have already been processed load them        
    if len(os.listdir(ts_data_dir)) > 0:
        print("... loading ts data from files")
        return({re.sub("\.csv","",cf)[3:]:pd.read_csv(os.path.join(ts_data_dir,cf)) for cf in os.listdir(ts_data_dir)})

    ## load the data
    dfs = {}
    dfs['all'] = df1
    for country in top_ten_countries(df):
        country_id = re.sub("\s+","_",country.lower())
        #file_name = os.path.join(data_dir,"ts-"+ country_id + ".csv")
        dfs[country_id] = convert_to_ts(df,country=country)

    ## save the data as csv    
    for key, item in dfs.items():
        item.to_csv(os.path.join(ts_data_dir,"ts-"+key+".csv"),index=False)
        
    return(dfs)

def fetch_ts_from_csv():
    """
    convenience function to read in new data
    uses csv to load quickly
    use clean=True when you want to re-create the files
    """

    ts_data_dir = os.path.join(".","ts-data")
    
    ## if files have already been processed load them        
    if len(os.listdir(ts_data_dir)) > 0:
        print("... loading ts data from files")
        return({re.sub("\.csv","",cf)[3:]:pd.read_csv(os.path.join(ts_data_dir,cf)) for cf in os.listdir(ts_data_dir)})

def engineer_features(df,training=True):
    ## extract dates
    dates = df['date'].values.copy()
    dates = dates.astype('datetime64[D]')
    print("\n dates")
    print(dates)
    
    ## engineer some features
    eng_features = defaultdict(list)
    previous =[7, 14, 28, 70]  #[7, 14, 21, 28, 35, 42, 49, 56, 63, 70]
    y = np.zeros(dates.size)
    for d,day in enumerate(dates):

        ## use windows in time back from a specific date
        for num in previous:
            current = np.datetime64(day, 'D') 
            #print("current: " + str(current))
            prev = current - np.timedelta64(num, 'D')
            #print("prev: " + str(prev))
            mask = np.in1d(dates, np.arange(prev,current,dtype='datetime64[D]'))
            eng_features["previous_{}".format(num)].append(df[mask]['revenue'].sum())

        ## get the target revenue    
        plus_30 = current + np.timedelta64(30,'D')
        mask = np.in1d(dates, np.arange(current,plus_30,dtype='datetime64[D]'))
        y[d] = df[mask]['revenue'].sum()

        ## attempt to capture monthly trend with previous years data (if present)
        start_date = current - np.timedelta64(365,'D')
        stop_date = plus_30 - np.timedelta64(365,'D')
        mask = np.in1d(dates, np.arange(start_date,stop_date,dtype='datetime64[D]'))
        eng_features['previous_year'].append(df[mask]['revenue'].sum())

        ## add some non-revenue features
        minus_30 = current - np.timedelta64(30,'D')
        mask = np.in1d(dates, np.arange(minus_30,current,dtype='datetime64[D]'))
        eng_features['recent_invoices'].append(df[mask]['unique_invoices'].mean())
        eng_features['recent_views'].append(df[mask]['total_views'].mean())

    X = pd.DataFrame(eng_features)
    ## combine features in to df and remove rows with all zeros
    X.fillna(0,inplace=True)
    mask = X.sum(axis=1)>0
    X = X[mask]
    y = y[mask]
    dates = dates[mask]
    X.reset_index(drop=True, inplace=True)

    if training == True:
        ## remove the last 30 days (because the target is not reliable)
        mask = np.arange(X.shape[0]) < np.arange(X.shape[0])[-30]
        X = X[mask]
        y = y[mask]
        dates = dates[mask]
        X.reset_index(drop=True, inplace=True)
    
    return(X,y,dates)   
