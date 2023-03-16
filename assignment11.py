##
## File: assignment11.py (STAT 3250)
## Topic: Assignment 11 
##

##  The file Stocks.zip is a zip file containing nearly 100 sets of price 
##  records for various stocks.  A sample of the type of files contained
##  in Stocks.zip is ABT.csv, which we have seen previously and is posted
##  in recent course materials. Each file includes daily data for a specific
##  stock, with stock ticker symbol given in the file name. Each line of
##  a file includes the following:
##
##   Date = date for recorded information
##   Open = opening stock price 
##   High = high stock price 
##   Low = low stock price 
##   Close = closing stock price 
##   Volume = number of shares traded
##   Adj Close = closing price adjusted for stock splits (ignored for this assignment)

##   The time interval covered varies from stock to stock. For many files
##   there are dates when the market was open but the data is not provided, so
##   those records are missing. Note that some dates are not present because the 
##   market is closed on weekends and holidays.  Those are not missing records.  

##  The Gradescope autograder will be evaluating your code on a subset 
##  of the set of files in the folder Stocks.  Your code needs to automatically 
##  handle all assignments to the variables q1, q2, ... to accommodate the 
##  reduced set, so do not copy/paste things from the console window, and
##  take care with hard-coding values. 

##  The autograder will contain a folder Stocks containing the stock data sets.
##  This folder will be in the working directory so your code should be written
##  assuming that is the case.


import pandas as pd # load pandas
import numpy as np # load numpy
pd.set_option('display.max_columns', 10) # Display 10 columns in console
import glob
import re

# '*.csv' selects files ending in '.csv'
filelist = glob.glob('Stocks/*.csv') # 'glob.glob' is the directory search

df = pd.DataFrame()  # empty dataframe
for file in filelist:
    newdf = pd.read_csv(file)  # read in the file
    newdf['Ticker'] = re.search(r'(Stocks\\)?(\w+).csv', file).group(2) # add ticker column
    df = pd.concat([df,newdf])  # concatenate to existing dataframe
df.index = range(len(df)) # reset index

## 1.  Find the mean for the Open, High, Low, and Close entries for all 
##     records for all stocks.  Give your results as a Series with index
##     Open, High, Low, Close (in that order) and the corresponding means
##     as values.

# subset columns, calculate means
q1 = df.loc[:,'Open':'Close'].mean()  # Series of means of Open, High, Low, and Close


## 2.  Find all stocks with an average Close price less than 30.  Give your
##     results as a Series with ticker symbol as index and average Close price. 
##     price as value.  Sort the Series from lowest to highest average Close
##     price.  (Note: 'MSFT' is the ticker symbol for Microsoft.  'MSFT.csv',
##     'Stocks/MSFT.csv' and 'MSFT ' are not ticker symbols.)

# subset Close, group by Ticker, calculate mean, sort values
d2 = df['Close'].groupby(df['Ticker']).mean().sort_values()
# subset < 30
q2 =  d2[d2 < 30]  # Series of stocks with average close less than 30


## 3.  Find the top-10 stocks in terms of the day-to-day volatility of the
##     price, which we define to be the mean of the daily differences 
##     High - Low for each stock. Give your results as a Series with the
##     ticker symbol as index and average day-to-day volatility as value. 
##     Sort the Series from highest to lowest average volatility.

# create Volatility column
df['Volatility'] = df['High'] - df['Low']
# group by Ticker, calculate mean, take 10 largest, keeping ties
q3 = df['Volatility'].groupby(df['Ticker']).mean().nlargest(10, keep='all')  # Series of top-10 mean volatility


## 4.  Repeat the previous problem, this time using the relative volatility, 
##     which we define to be the mean of
## 
##                       (High − Low)/(0.5(Open + Close))
##
##     for each day. Provide your results as a Series with the same specifications
##     as in the previous problem.

# create Rel_Volatility column
df['Rel_Volatility'] = (df['High'] - df['Low']) / (0.5 * (df['Open'] + df['Close']))
# group by Ticker, calculate mean, take 10 largest, keeping ties
q4 = df['Rel_Volatility'].groupby(df['Ticker']).mean().nlargest(10, keep='all')  # Series of top-10 mean relative volatility


## 5.  For each day the market was open in October 2008, find the average 
##     daily Open, High, Low, Close, and Volume for all stocks that have
##     records for October 2008.  (Note: The market is open on a given
##     date if there is a record for that date in any of the files.)
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close, Volume (in that order).  The dates should 
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2008-10-01, the same form as in the files.   

# convert Date into a datetime column
df['Date'] = pd.to_datetime(df['Date'])
# subset records from Oct 2008
oct_2008 = df.loc[(df['Date'] > pd.Timestamp(2008, 9, 30)) & (df['Date'] < pd.Timestamp(2008, 11, 1)),:]
# subset columns, group by Ticker, calculate means
q5 = oct_2008.loc[:,'Open':'Volume'].groupby(oct_2008['Date'].dt.strftime('%Y-%m-%d')).mean()  # DataFrame of means for each open day of Oct '08.


## 6. For 2011, find the date with the maximum average relative volatility 
##    for all stocks and the date with the minimum average relative 
##    volatility for all stocks. Give your results as a Series with 
##    the dates as index and corresponding average relative volatility
##    as values, with the maximum first and the minimum second.

# subset records from 2011
df_2011 = df.loc[df['Date'].dt.year == 2011,:]
# subset Rel_Volatility, group by Date, calculate mean
t6 = df_2011['Rel_Volatility'].groupby(df_2011['Date'].dt.strftime('%Y-%m-%d')).mean()
# create a series with indeces index of max and index of min and values max and min
q6 = pd.Series({t6.idxmax():t6.max(), t6.idxmin():t6.min()})  # Series of average relative volatilities


## 7. For 2010-2012, find the average relative volatility for all stocks on
##    Monday, Tuesday, ..., Friday.  Give your results as a Series with index
##    'Mon','Tue','Wed','Thu','Fri' (in that order) and corresponding
##    average relative volatility as values. 

# subset records from 2010-2012
df_2010_2012 = df.loc[df['Date'].dt.year.isin(range(2010,2013)),:]
# create days list for ordering
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
# subset Rel_Volatility, group by Date, calculate mean, reorder index using days
q7 = df_2010_2012['Rel_Volatility'].groupby(df_2010_2012['Date'].dt.strftime('%a')).mean().reindex(days)  # Series of average relative volatility by day of week


## 8.  For each month of 2009, determine which stock had the maximum average 
##     relative volatility. Give your results as a Series with MultiIndex
##     that includes the month (month number is fine) and corresponding stock 
##     ticker symbol (in that order), and the average relative volatility
##     as values.  Sort the Series by month number 1, 2, ..., 12.

# subset records from 2009
df_2009 = df.loc[df['Date'].dt.year == 2009,:]
# subset Rel_Volatility, group by month and Ticker, calculate mean,
# group by Date, take largest
q8 = df_2009['Rel_Volatility'].groupby([df_2009['Date'].dt.month, df_2009['Ticker']]).mean().groupby('Date', group_keys=False).nlargest(1)  # Series of maximum relative volatilities by month


## 9.  The “Python Index” is designed to capture the collective movement of 
##     all of our stocks. For each date, this is defined as the average price 
##     for all stocks for which we have data on that day, weighted by the 
##     volume of shares traded for each stock.  That is, for stock values 
##     S_1, S_2, ... with corresponding volumes V_1, V_2, ..., the average
##     weighted volume is
##
##           (S_1*V_1 + S_2*V_2 + ...)/(V_1 + V_2 + ...)
##
##     Find the Open, High, Low, and Close for the Python Index for each date
##     the market was open in January 2013. 
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close (in that order).  The dates should 
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2013-01-31, the same form as in the files.   

# subset records from Jan 2013, select columns
d9 = df.loc[(df['Date'].dt.year == 2013) & (df['Date'].dt.month == 1),'Date':'Volume']
# Create Total columns for math operations later
d9.loc[:,['Open_Total', 'High_Total', 'Low_Total', 'Close_Total']] = d9.loc[:,'Open':'Close'].transform(lambda x: x*d9['Volume']).rename(columns={'Open': 'Open_Total', 'High': 'High_Total', 'Low': 'Low_Total', 'Close': 'Close_Total'})
# group by date, calculate sums
d9_b = d9.groupby(d9['Date'].dt.strftime('%Y-%m-%d')).sum()
# create data frame of Python Index values
q9 = pd.DataFrame({
    'Open': d9_b['Open_Total'] / d9_b['Volume'],
    'High': d9_b['High_Total'] / d9_b['Volume'],
    'Low': d9_b['Low_Total'] / d9_b['Volume'],
    'Close': d9_b['Close_Total'] / d9_b['Volume']
}) # DataFrame of Python Index values for each open day of Jan 2013. 


## 10. For the years 2007-2012 determine the top-8 month-year pairs in terms 
##     of average relative volatility of the Python Index. Give your results
##     as a Series with MultiIndex that includes the month (month number is 
##     fine) and year (in that order), and the average relative volatility
##     as values.  Sort the Series by average relative volatility from
##     largest to smallest.

# subset records from 2007-2012, select columns
df_2007_2012 = df.loc[df['Date'].dt.year.isin(range(2007,2013)), 'Date':'Volume']
# Create Total columns for math operations later
df_2007_2012.loc[:,['Open_Total', 'High_Total', 'Low_Total', 'Close_Total']] = df_2007_2012.loc[:,'Open':'Close'].transform(lambda x: x*df_2007_2012['Volume']).rename(columns={'Open': 'Open_Total', 'High': 'High_Total', 'Low': 'Low_Total', 'Close': 'Close_Total'})
# group by date, calculate sums
d10a = df_2007_2012.groupby(df_2007_2012['Date'].dt.strftime('%Y-%m-%d')).sum()
# create data frame of Python Index values
d10b = pd.DataFrame({
    'Open': d10a['Open_Total'] / d10a['Volume'],
    'High': d10a['High_Total'] / d10a['Volume'],
    'Low': d10a['Low_Total'] / d10a['Volume'],
    'Close': d10a['Close_Total'] / d10a['Volume']
}).reset_index(level=0)
# calcuate Rel_Volatility column
d10b['Rel_Volatility'] = (d10b['High'] - d10b['Low']) / (0.5 * (d10b['Open'] + d10b['Close']))
# group by year and month, calculate mean, keep 8 largest, including ties
q10 = d10b['Rel_Volatility'].groupby([pd.to_datetime(d10b['Date']).dt.month, pd.to_datetime(d10b['Date']).dt.year]).mean().nlargest(8, keep='all')  # Series of month-year pairs and average rel. volatilities


## 11. Each stock in the data set contains records starting at some date and 
##     ending at another date.  In between the start and end dates there may be 
##     dates when the market was open but there is no record -- these are the
##     missing records for the stock.  For each stock, determine the percentage
##     of records that are missing out of the total records that would be
##     present if no records were missing. Give a Series of those stocks
##     with less than 1.3% of records missing, with the stock ticker as index 
##     and the corresponding percentage as values, sorted from lowest to 
##     highest percentage.

# Get all dates when the market was open
market_open = pd.Series(df['Date'].unique())
# get the start date, end date, and number of records for each ticker and put
# them in a dataframe
d11 = pd.DataFrame({
    'Start_Date': df['Date'].groupby(df['Ticker']).min(),
    'End_Date': df['Date'].groupby(df['Ticker']).max(),
    'n_Records': df['Date'].groupby(df['Ticker']).count()
})
# calculate how many days each ticker could have had records
d11['n_Days'] = d11.loc[:, 'Start_Date':'End_Date'].apply(lambda x: market_open.loc[(market_open >= x['Start_Date']) & (market_open <= x['End_Date'])].size, axis=1)
# calculate percent of possible days where there were not records
t11 = 100 * (d11['n_Days'] - d11['n_Records']) / d11['n_Days']
# filter < 1.3 and sort descending
q11 = t11[t11 < 1.3].sort_values()  # Series of stocks and percent missing

