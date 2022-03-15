##
## File: assignment03.py (STAT 3250)
## Topic: Assignment 3 
##

##  The questions in this assignment refer to the data in the
##  file 'absent.csv'.  The data contains 740 records from an
##  employer, with 21 columns of data for each record.  (There
##  are a few missing values indicated by zeros where zeros 
##  are clearly not appropriate.)  The file 'absent.pdf' has
##  a summary of the meanings for the variables.
##
##  All of these questions can be completed without loops.  You 
##  should try to do them this way, "code efficiency" will take 
##  this into account.

import numpy as np  # load numpy as np
import pandas as pd # load pandas as pd

absent = pd.read_csv('absent.csv')  # import the data set as a pandas dataframe

## 1.  Find the mean absent time among all records.

# calculate means and subset Absenteeism column
q1 = np.mean(absent)['Absenteeism time in hours']


## 2.  Determine the number of records corresponding to
##     being absent on a Thursday.

# create T/F array and sum trues
q2 = np.sum(absent['Day of the week'] == 5)


## 3.  Find the number of unique employees IDs represented in 
##     this data.  

# find unique employee IDs and get its size
q3 = np.unique(absent['ID']).size


## 4.  Find the average transportation expense for the employee 
##     with ID = 34.

# find records corresponding to employee ID 34, take the column means,
# and subset the Transportation expense column
q4 = np.mean(absent.loc[absent['ID'] == 34])['Transportation expense']


## 5.  Find the total number of hours absent for the records
##     for employee ID = 11.

# find records corresponding to employee ID 11, take the column sums,
# and subset the Absenteeism time in hours column
q5 = np.sum(absent.loc[absent['ID'] == 11])['Absenteeism time in hours']


## 6.  Find (a) the mean number of hours absent for the records of those who 
##     have no pets, then (b) do the same for those who have more than one pet.

# replace number of pets greater than 1 with 2, group by Pet, calculate means,
# and subset appropriate ones
absent.loc[absent['Pet'] > 1, 'Pet'] = 2
grouped_means = absent['Absenteeism time in hours'].groupby(absent['Pet']).mean()
q6a = grouped_means[0]
q6b = grouped_means[2]


## 7.  Among the records for absences that exceeded 8 hours, find (a) the 
##     proportion that involved smokers.  Then (b) do the same for absences 
##     of no more then 4 hours.

# subset the Social smoker column for the absenteeism time range, then divide
# the number of trues by the total number
over_8_smoker_col = absent.loc[absent['Absenteeism time in hours'] > 8, 'Social smoker']
q7a = over_8_smoker_col.sum()/over_8_smoker_col.size
under_4_smoker_col = absent.loc[absent['Absenteeism time in hours'] <= 4, 'Social smoker']
q7b = under_4_smoker_col.sum()/under_4_smoker_col.size

## 8.  Repeat Question 7, this time for social drinkers in place of smokers.

# subset the Social drinker column for the absenteeism time range, then divide
# the number of trues by the total number
over_8_drinker_col = absent.loc[absent['Absenteeism time in hours'] > 8, 'Social drinker']
q8a = over_8_drinker_col.sum()/over_8_drinker_col.size
under_4_drinker_col = absent.loc[absent['Absenteeism time in hours'] <= 4, 'Social drinker']
q8b = under_4_drinker_col.sum()/under_4_drinker_col.size


## 9.  Find the top-5 employee IDs in terms of total hours absent.  Give
##     the IDs and corresponding total hours absent as a Series with ID
##     for the index, sorted by the total hours absent from most to least.

# group time column by ID, sum, sort the values in descending order, and subset
# the top 5
q9 = absent['Absenteeism time in hours'].groupby(absent['ID']).sum().sort_values(ascending=False).iloc[:5]


## 10. Find the average hours absent per record for each day of the week.
##     Give the day number and average as a Series with the day number
##     as the index, sorted by day number from smallest to largest.

# group time column by Day of the week, take means
q10 = absent['Absenteeism time in hours'].groupby(absent['Day of the week']).mean()


## 11. Repeat Question 10 replacing day of the week with month.
##     Give the month number and average as a Series with the month number
##     as the index, sorted by month number from smallest to largest.

# group time column by Month of absence, take means and remove month 0 because
# it doesn't make any sense
q11 = absent['Absenteeism time in hours'].groupby(absent['Month of absence']).mean().loc[1:]


## 12. Find the top 3 most common reasons for absence for the social smokers.
##      Give the reason code and number of occurances as a Series with the 
##      reason code as the index, sorted by number of occurances from
##      largest to smallest.  (If there is a tie for 3rd place,
##      include all that tied for that position.)

# subset arbitrary column where Social smoker is true, group by Reason for
# absence, count occurences, and sort descending. Then subset the series, only
# taking observations where the value is >= the 3rd value
reason_freqs = absent.loc[absent['Social smoker'] == 1, 'ID'].groupby(absent['Reason for absence']).count().sort_values(ascending=False)
q12 = reason_freqs.loc[reason_freqs >= reason_freqs.iloc[2]]

