##
## File: assignment05.py (STAT 3250)
## Topic: Assignment 5 
##

##  This assignment requires the data file 'diabetic_data.csv'.  This file
##  contains records for over 100,000 hospitalizations for people who have
##  diabetes.  The file 'diabetic_info.pdf' contains information on the
##  codes used for a few of the entries.  Missing values are indicated by
##  a '?'.  You should be able to read in this file using the usual 
##  pandas methods.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the diabetic_data.csv data that includes about 35% of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values. 

##  Note: Many of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). Scoring will take
##  this into account.

import pandas as pd # load pandas as pd

dia = pd.read_csv('diabetic_data.csv')
dia1 = dia.loc[:10,:]

## 1.  Determine the average number of procedures ('num_procedures') for 
##     those classified as females and for those classified as males.

# group by gender, calculate the mean, select num_procedures column, pull out
# female and male numbers
tmp1 = dia.groupby('gender').mean()['num_procedures']
q1f = tmp1['Female']  # female average number of procedures
q1m = tmp1['Male']  # male average number of procedures


## 2.  Determine the average length of hospital stay ('time_in_hospital')
##     for each race classification.  (Omit those unknown '?' but include 
##     those classified as 'Other'.)  Give your answer as a Series with
##     race for the index sorted alphabetically.
# select rows without ? in race column, group by race, calculate the mean,
# select time_in_hospital column, sort by index alphabetically
tmp2 = dia.loc[dia['race'] != '?',:].groupby('race').mean()['time_in_hospital'].sort_index()
q2 = tmp2  # Series of average length of stay by race


## 3.  Determine the percentage of total days spent in the hospital due to
##     stays ("time_in_hospital") of at least 7 days. (Do not include the %
##     symbol in your answer.)

# calculate number of days in stays 7 days or longer
num3 = dia.loc[dia['time_in_hospital'] >= 7,'time_in_hospital'].sum()
# calculate total number of days in all stays
denom3 = dia['time_in_hospital'].sum()
# multiply numerator by 100 and divide by denominator
q3 = 100 * num3 / denom3  # percentage of days from stays of at least 7 days


## 4.  Among the patients in this data set, what percentage had at least
##     three recorded hospital visits?  Each distinct record can be assumed 
##     to be for a separate hospital visit. Do not include the % symbol in
##     your answer.

# group by patient_nbr and get count of visits for each patient
tmp4 = dia['patient_nbr'].groupby(dia['patient_nbr']).count()
# calculate number of patients with 3 or more visits
num4 = len(tmp4.loc[tmp4 >= 3])
# calculate number of patients
denom4 = len(tmp4)
# multiply numerator by 100 and divide by denominator
q4 = 100 * num4 / denom4  # percentage patients with at least three visits


## 5.  List the top-15 most common diagnoses, based on the codes listed 
##     collectively in the columns 'diag_1', 'diag_2', and 'diag_3'.
##     Give your response as a Series with the diagnosis code as the 
##     index and the number of occurances as the values, sorted by
##     values from largest to smallest.  If more than one value could
##     go in the 15th position, include all that could go in that 
##     position.  (This is the usual "include ties" policy.)

# count the frequency of each diagnosis
diag_1_counts = dia['diag_1'].groupby(dia['diag_1']).count()
diag_2_counts = dia['diag_2'].groupby(dia['diag_2']).count()
diag_3_counts = dia['diag_3'].groupby(dia['diag_3']).count()
# add all series together, using 0 for missing values
tmp5 = diag_1_counts.add(diag_2_counts, fill_value=0).add(diag_3_counts, fill_value=0).sort_values(ascending=False)
# find everything greater than or equal to the 15th value
q5 = tmp5[tmp5 >= tmp5[14]]  # top-15 diagnoses plus any ties


## 6.  The 'age' in each record is given as a 10-year range of ages.  Assume
##     that the age for a person is the middle of the range.  (For instance,
##     those with 'age' [40,50) are assumed to be 45.)  Determine the average
##     age for each classification in the column 'acarbose'.  Give your
##     answer as a Series with the classification as index and averages as
##     values, sorted from largest to smallest average.

# create age2 column which contains the midpoint of the age range
dia['age2'] = dia['age'].str[1:3].str.replace('-', '').astype(int) + 5
# group by acarbose, calculate means, subset age2 column, sort values
q6 = dia.groupby('acarbose').mean()['age2'].sort_values(ascending=False)  # Series of classifications and averages


## 7.  Determine all medical specialties that have an average hospital stay
##     (based on time_in_hospital) of at least 7 days.  Give a Series with
##     specialty as index and average hospital stay as values, sorted from
##     largest to smallest average stay.

# group by medical specialty, calculate means, and subset time in hospital
tmp7 = dia.groupby('medical_specialty').mean()['time_in_hospital']
# subset all avg stays >= 7, sort values
q7 = tmp7[tmp7 >= 7].sort_values(ascending=False)  # Series of specialities and average stays


##  8. Three medications for type 2 diabetes are 'glipizide', 'glimepiride',
##     and 'glyburide'.  There are columns in the data for each of these.
##     Determine the number of records for which at least two of these
##     are listed as 'Steady'.

tmp8 = (dia['glipizide']+dia['glimepiride']+dia['glyburide']).str.count('Steady')
q8 = len(tmp8[tmp8 >=2])  # number of records with at least two 'Steady'


##  9. Find the percentage of "time_in_hospital" accounted for by the top-100 
##     patients in terms of number of times in file.  (Include all patients 
##     that tie the 100th patient.)

# group by patient, count number of entries, sort
tmp9a = dia.groupby('patient_nbr').size().sort_values(ascending=False)
# subset top 100
patients9 = tmp9a.nlargest(100, keep='all').index
# group by patient, calculate sums, subset time_in_hospital column
tmp9b = dia.groupby('patient_nbr').sum()['time_in_hospital']
# sum hours for patients in the top 100
num9 = tmp9b.loc[tmp9b.index.isin(patients9)].sum()
# sum hours for all patients
denom9 = tmp9b.sum()
# compute percentage
q9 = 100 * num9 / denom9  # Percentage of time from top-100 patients


## 10. What percentage of reasons for admission ('admission_source_id')
##     correspond to some form of transfer from another care source?

# count number of entries with the transfer codes
num10 = dia.loc[dia['admission_source_id'].isin([4, 5, 6, 10, 18, 22, 25, 26]),:].size
# compute percentage, with denominator as total number of entries
q10 = 100 * num10 / dia.size  # Percentage of admission by transfer


## 11. The column 'discharge_disposition_id' gives codes for discharges.
##     Determine the 5 codes that resulted in the greatest percentage of
##     readmissions.  Give your answer as a Series with discharge code
##     as index and readmission percentage as value, sorted by percentage
##     from largest to smallest.

# subset where readmitted is not NO, group by discharge_disposition_id,
# count entries
num11 = dia.loc[dia['readmitted'] != 'NO'].groupby(['discharge_disposition_id']).size()
# group by discharge_disposition_id, count entries
denom11 = dia.groupby(['discharge_disposition_id']).size()
# compute percentages, sort, select top 5
q11 = (100 * num11 / denom11).sort_values(ascending=False).iloc[:5]  # Series of discharge codes and readmission percentages


## 12. The columns from 'metformin' to 'citoglipton' are all medications, 
##     with "Up", "Down", and "Steady" indicating the patient is taking that 
##     medication.  For each of these medications, determine the average
##     number of medications from this group that patients are taking.
##     Give a Series of all medications with an average of at least 1.5,
##     with the medications as index and averages as values, sorted 
##     largest to smallest average.
##     (Hint: df.columns gives the column names of the data frame df.)

# create df of just medicine columns transformed into Boolean values
# True: taking medication
# False: not taking medication
df12 = dia.loc[:,'metformin':'citoglipton'] != 'No'
# initialize output values list
output = [0]*df12.columns.size
# loop through indeces of columns of df12
for i in range(df12.columns.size):
    # subsets rows where the current column is True, sums those rows, and
    # calculates the mean of the sums
    # the resulting value is stored in output[i]
    output[i] = df12.loc[df12[df12.columns[i]],:].sum(axis=1).mean()
# creates a Series where values come from output and indeces from df12.columns
tmp12 = pd.Series(output, df12.columns)
# subset values where the mean number of medications >= 1.5, sort
q12 = tmp12[tmp12 >= 1.5].sort_values(ascending=False)  # Series of medications and averages

