##
## File: assignment13.py (STAT 3250)
## Topic: Assignment 13 
##


##  These questions are similar to reviewed lecture material, but 
##  provide some experience with Dask.

import dask.dataframe as dd #import libraries
from dask.diagnostics import ProgressBar
import numpy as np
import pandas as pd
import time

dtypes = {
 'Date First Observed': str, 'Days Parking In Effect    ': str,
 'Double Parking Violation': str, 'Feet From Curb': np.float32,
 'From Hours In Effect': str, 'House Number': str,
 'Hydrant Violation': str, 'Intersecting Street': str,
 'Issue Date': str, 'Issuer Code': np.float32,
 'Issuer Command': str, 'Issuer Precinct': np.float32,
 'Issuer Squad': str, 'Issuing Agency': str,
 'Law Section': np.float32, 'Meter Number': str,
 'No Standing or Stopping Violation': str,
 'Plate ID': str, 'Plate Type': str,
 'Registration State': str, 'Street Code1': np.uint32,
 'Street Code2': np.uint32, 'Street Code3': np.uint32,
 'Street Name': str, 'Sub Division': str,
 'Summons Number': np.uint32, 'Time First Observed': str,
 'To Hours In Effect': str, 'Unregistered Vehicle?': str,
 'Vehicle Body Type': str, 'Vehicle Color': str,
 'Vehicle Expiration Date': str, 'Vehicle Make': str,
 'Vehicle Year': np.float32, 'Violation Code': np.uint16,
 'Violation County': str, 'Violation Description': str,
 'Violation In Front Of Or Opposite': str, 'Violation Legal Code': str,
 'Violation Location': str, 'Violation Post Code': str,
 'Violation Precinct': np.float32, 'Violation Time': str
}

nyc = dd.read_csv('nyc-parking-tickets2015.csv', dtype=dtypes, usecols=dtypes.keys())
# nyc = dd.read_csv('nyc_short.csv', dtype=dtypes, usecols=dtypes.keys())

# with ProgressBar(): makes it use a pretty progress bar while running so I
# could make sure the code didn't get stuck anywhere

## 1.  There are several missing values in the 'Vehicle Body Type' column. Impute 
##     missing values of 'Vehicle Body Type' with the mode. What is the mode?

with ProgressBar():
    # calculate the mode, take first item
    q1 = nyc['Vehicle Body Type'].mode().compute()[0] # Report the mode, the most common Vehicle Body Type.
# fill na values in Vehicle Body Type with the mode
nyc = nyc.fillna({'Vehicle Body Type': q1})
print(f'q1={q1}')


## 2.  How many missing data points are there in the 'Intersecting Street' column?

with ProgressBar():
    # subset missing values of Intersecting Street, get size
    q2 = nyc.loc[nyc['Intersecting Street'].isna(), 'Intersecting Street'].compute().size # Number of missing data points
print(f'q2={q2}')


## 3.  What percentage of vehicle makes are Jeeps during the months of March - 
##     September (inclusive) of 2015?

with ProgressBar():
    # convert Issue Date to datetime
    meta = ('Issue Date', 'datetime64[ns]')
    nyc['Issue Date'] = nyc['Issue Date'].map_partitions(pd.to_datetime, meta=meta)
    # subset Vehicle Make from 2015 between March and September, value_counts
    # using normalize, subset JEEP
    q3 = 100 * nyc.loc[(nyc['Issue Date'].dt.year == 2015) & (nyc['Issue Date'].dt.month >= 3) & (nyc['Issue Date'].dt.month <= 9),'Vehicle Make'].compute().value_counts(normalize=True)['JEEP'] # Percentage of Jeeps
print(f'q3={q3}')


## 4.  What's the most common color of a car in 2015? Maintain the color in all caps.

with ProgressBar():
    # subset 2015 Vehicle Color, value_counts, get first level of index for
    # largest value
    q4 = nyc.loc[(nyc['Issue Date'].dt.year == 2015),'Vehicle Color'].compute().value_counts().nlargest(1).index[0] # Most common car color
print(f'q4={q4}')


## 5.  Find all the cars in any year that are the same color as q4. What percentage of 
##     those care are sedans?

with ProgressBar():
    # subset Vehicle Body Type of white cars, value_counts using normalize
    white_car_types = nyc.loc[nyc['Vehicle Color'] == 'WHITE', 'Vehicle Body Type'].value_counts(normalize=True).compute()
    # select sedans, multiply proportion by 100
    q5 = 100 * white_car_types['SDN'] # Percentage of sedans
print(f'q5={q5}')


## 6.  Make a table of the top 5 registration states, sorted greatest to least.

with ProgressBar():
    # subset Registration State, value_counts, get 5 largest
    q6 = nyc['Registration State'].value_counts().nlargest(5).compute() # Series of top 5 registration states
print(f'q6={q6}')


## 7.  Perhaps someone bought a new vehicle and kept the same license plate. How many license 
##     plates have more than one 'Vehicle Make' associated with the respective plate?

with ProgressBar():
    # subset where Plate ID is not BLANKPLATE, keep Plate ID and Vehicle Make cols
    # drop duplicate rows to count unique combinations of plates and makes
    nyc_sub = nyc.loc[nyc['Plate ID'] != 'BLANKPLATE', ['Plate ID', 'Vehicle Make']].drop_duplicates()
    # value_counts Plate ID (if one appears multiple times it must be a
    # different Vehicle Make bc of drop_duplicates), check if >1, sum Booleans,
    # convert from np.int64 to int
    q7 = int((nyc_sub['Plate ID'].value_counts().compute() > 1).sum()) # Number of license plates
print(f'q7={q7}')


# 8.  Determine the top three hours that result in the most parking violations. 
#     "0011A" would be 12:11 AM and "0318P" would be 3:18 PM. Report the solution 
#     with the index in the format of "01A" and the count.

with ProgressBar():
    # create Violation_Hour column with first 2 digits, A or P
    nyc = nyc.assign(Violation_Hour=lambda df: df['Violation Time'].str.extract(r'(\d{2})\d{2}[AP]') + df['Violation Time'].str.extract(r'([AP])'))
    # value_counts, take 3 largest
    q8 = nyc['Violation_Hour'].value_counts().nlargest(3).compute() # Series with top three hours
print(f'q8={q8}')


## 9.  Among the tickets issued by Precinct 99, what is the average distance from the
##     curb in feet?

with ProgressBar():
    # subset Feet From Curb where violation Precinct is 99, compute mean
    q9 = nyc.loc[nyc['Violation Precinct'] == 99, 'Feet From Curb'].mean().compute() # Average distance from the curb
print(f'q9={q9}')

