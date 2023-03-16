##
## File: assignment09.py (STAT 3250)
## Topic: Assignment 9 
##

##  This assignment requires the data file 'airline-stats.txt'.  This file 
##  contains thousands of records of aggregated flight information, organized 
##  by airline, airport, and month.  The first record is shown below.  
##
##  The file is quite large (1.8M lines, 31MB) so may be difficult to open in
##  Spyder.  An abbreviated version 'airline-stats-brief.txt' is also 
##  provided that has the same structure as the original data set but is
##  easier to open in Spyder.

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the airline-stats.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

# =============================================================================
# airport
#     code: ATL 
#     name: Atlanta GA: Hartsfield-Jackson Atlanta International
# flights 
#     cancelled: 5 
#     on time: 561 
#     total: 752 
#     delayed: 186 
#     diverted: 0
# number of delays 
#     late aircraft: 18 
#     weather: 28 
#     security: 2
#     national aviation system: 105 
#     carrier: 34
# minutes delayed 
#     late aircraft: 1269 
#     weather: 1722 
#     carrier: 1367 
#     security: 139 
#     total: 8314 
#     national aviation system: 3817
# dates
#     label: 2003/6 
#     year: 2003 
#     month: 6
# carrier
#     code: AA 
#     name: American Airlines Inc.
# =============================================================================

import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

# Read in the test data as text all at once, split on separators
airlines = pd.Series(open('airline-stats.txt').read().split('##########\n##########')).str.strip()
def format_airline(airline):
    """
    This function takes in the text data for an airline and converts it to a
    dictionary for use in creating a data frame
    
    parameters:
        airline: a string containing data for one airline
    output: a dictionary containing the same information
    """
    # concatenate category labels to beginning of information labels
    # ex.
    # [airport, code: ATL, name: Atlanta GA: Hartsfield-Jackson Atlanta International]
    # is converted to
    # [airport_code: ATL, airport_name: Atlanta GA: Hartsfield-Jackson Atlanta International]
    last_label = ''
    new_list = []
    for line in airline.splitlines():
        # check if it is a category label
        if line.find(':') == -1:
            # if so, set to last_label
            last_label = line.strip()
        else:
            # if not, append {last_label}_{line.strip()}
            new_list.append(f'{last_label}_{line.strip()}')
    # create dictionary, splitting each element on : and using the first element
    # as the key and the second element of the value. Strip each value and
    # replace spaces with underscores
    return {line.split(':')[0].strip().replace(' ', '_'):line.split(':')[len(line.split(':'))-1].strip() for line in new_list}
airlines2 = pd.json_normalize(airlines.transform(lambda x: format_airline(x)))
# Set all types explicitly
airlines2 = airlines2.astype({
    'airport_code': str,
    'airport_name': str,
    'flights_cancelled': int,
    'flights_on_time': int,
    'flights_total': int,
    'flights_delayed': int,
    'flights_diverted': int,
    'number_of_delays_late_aircraft': int,
    'number_of_delays_weather': int,
    'number_of_delays_security': int,
    'number_of_delays_national_aviation_system': int,
    'number_of_delays_carrier': int,
    'minutes_delayed_late_aircraft': int,
    'minutes_delayed_weather': int,
    'minutes_delayed_carrier': int,
    'minutes_delayed_security': int,
    'minutes_delayed_total': int,
    'minutes_delayed_national_aviation_system': int,
    'dates_label': str,
    'dates_year': str,
    'dates_month': str,
    'carrier_code': str,
    'carrier_name': str
})
# format date column
airlines2['date'] = pd.to_datetime(airlines2['dates_label'], format='%Y/%m')
airlines3 = airlines2.drop(columns=['dates_label','dates_year','dates_month'])

## 1.  Give the total number of hours delayed for all flights in all records,
##     based on the entries in (minutes delayed)/total

# sum minutes delayed column, divide by 60
q1 = airlines3['minutes_delayed_total'].sum() / 60  # total number of hours delayed for all flights in all records


## 2.  Which airlines appear in at least 500 records?  Give a Series with airline
##     names as index and record counts for values, in order of record count 
##     from largest to smallest.

# group by carrier name, value counts
t2 = airlines3['carrier_name'].value_counts()
# filter greater than or equal to 500
q2 = t2[t2 >= 500]  # Series of airline names and record counts
   

## 3.  The entry under 'flights/delayed' is not always the same as the total
##     of the entries under 'number of delays'.  (The reason for this is not
##     clear.)  Determine the percentage of records for which these two
##     values are different.

# create logical vector for equality between flights delayed and the sum of
# specific delay causes, value counts using normalize, subset False, multiply by 100
q3 = 100 * (airlines3['flights_delayed'] == airlines3.loc[:,'number_of_delays_late_aircraft':'number_of_delays_carrier'].sum(axis=1)).value_counts(normalize=True)[False]  # percentage of records with two values different


## 4.  Determine the percentage of records for which the number of delays due to
##     'late aircraft' exceeds the number of delays due to 'carrier'.

# create logical vector for late aircraft > carrier, value counts using normalize,
# subset True, multiply by 100
q4 = 100 * (airlines3['number_of_delays_late_aircraft'] > airlines3['number_of_delays_carrier']).value_counts(normalize=True)[True]  # percentage of records as described above


## 5.  Find the top-8 airports in terms of the total number of minutes delayed.
##     Give a Series with the airport names (not codes) as index and the total 
##     minutes delayed as values, sorted order from largest to smallest total.
##     (Include any ties for 8th position as usual)

# group by airport_name, subset minutes_delayed_total, sum, take 8 larget, keeping ties
q5 = airlines3.groupby('airport_name')['minutes_delayed_total'].sum().nlargest(8, keep='all')  # Series of airport names and total minutes delayed


## 6.  Find the top-12 airports in terms of rates (as percentages) of on-time flights.
##     Give a Series of the airport names (not codes) as index and percentages
##     as values, sorted from largest to smallest percentage. (Include any
##     ties for 12th position as usual)

# group by airport_name, sum
s6 = airlines3.groupby('airport_name').sum()
# take sum of flights on time over sum of flights total, multiply by 100, take
# 12 larget, keeping ties
q6 = (100 * s6['flights_on_time'] / s6['flights_total']).nlargest(12, keep='all')  # Series of airport names and percentages 


## 7.  Find the top-10 airlines in terms of rates (as percentages) of on time flights.
##     Give a Series of the airline names (not codes) as index and percentages  
##     as values, sorted from largest to smallest percentage. (Include any
##     ties for 10th position as usual)

# group by carrier name, sum
s7 = airlines3.groupby('carrier_name').sum()
# take sum of flights on time over sum of flights total, multiply by 100, take
# 10 larget, keeping ties
q7 = (100 * s7['flights_on_time'] / s7['flights_total']).nlargest(10, keep='all')  # Series of airline names and percentages


## 8.  Determine the average length (in minutes) by airline of a delay due
##     to the national aviation system.  Give a Series of airline name (not 
##     code) as index and average delay lengths as values, sorted from largest 
##     to smallest average delay length.

# group by carrier name, sum
s8 = airlines3.groupby('carrier_name').sum()
# take sum of minutes delayed over sum of total delays
avg_length_nas = s8['minutes_delayed_national_aviation_system'] / s8['number_of_delays_national_aviation_system']
# sort descending
q8 = avg_length_nas.sort_values(ascending=False)  # Series of airline names and average delay times


## 9.  For each month, determine the rates (as percentages) of flights delayed 
##     by weather. Give a Series sorted by month (1, 2, ..., 12) with the 
##     corresponding percentages as values.

# group by month, sum
s9 = airlines3.groupby(airlines3['date'].dt.month).sum()
# take sum number of delays over sum total flights, multiply by 100
q9 = 100 * s9['number_of_delays_weather'] / s9['flights_total']  # Series of months and percentages


## 10. Find all airports where the average length (in minutes) of 
##     security-related flight delays exceeds 35 minutes.  Give a Series with  
##     airport names (not codes) as index and average delay times as values, 
##     sorted from largest to smallest average delay.

# group by airport name, sum
s10 = airlines3.groupby('airport_name').sum()
# take sum minutes delayed over sum number of delays
avg_length_security = s10['minutes_delayed_security'] / s10['number_of_delays_security']
# subset greater than 35, sort values descending
q10 = avg_length_security.loc[avg_length_security > 35].sort_values(ascending=False)  # Series or airport names and average delay times


## 11. For each year, determine the airport that had the highest rate (as a 
##     percentage) of delays.  Give a Series with the years (least recent at top)  
##     and airport names (not code) as MultiIndex and the percentages as values.

# group by year and airport name, sum
s11 = airlines3.groupby([airlines3['date'].dt.year, airlines3['airport_name']]).sum()
# create delay rate entry, which is sum flights delayed over sum total flights
# multiplied by 100
s11['delay_rate'] = 100 * s11['flights_delayed'] / s11['flights_total']
# group by year, don't take group keys, select largest value for each year
q11 = s11['delay_rate'].groupby('date', group_keys=False).nlargest(1)  # Series of years/airport names and percentages


## 12. For each airline, determine the airport where that airline had its 
##     greatest percentage of delayed flights.  Give a Series with airline
##     names (not code) and airport names (not code) as MultiIndex and the
##     percentage of delayed flights as values, sorted from smallest to
##     largest percentage.

# group by carrier name and airport name, sum
s12 = airlines3.groupby(['carrier_name', 'airport_name']).sum()
# create delay rate entry, which is sum flights delayed over sum total flights
# multiplied by 100
s12['delay_rate'] = (100 * s12['flights_delayed'] / s12['flights_total'])
# group by carrier name, don't take group keys, select largest value for each
# year, sort values ascending
q12 = s12['delay_rate'].groupby('carrier_name', group_keys=False).nlargest(1).sort_values()  # Series of airline/airport and percentages


