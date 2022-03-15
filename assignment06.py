##
## File: assignment06.py (STAT 3250)
## Topic: Assignment 6
##

##  The questions this assignment are based on "timing_log.txt".
##  The file "timing_log.txt" contains the set of all WeBWorK
##  log entries on April 1, 2011.  The entries are organized by
##  one log entry per line, with each line including the following:
##
##  --the date and time of the entry
##  --a number that is related to the user (but is not unique)
##  --something that appears to be the epoch time stamp
##  --a hyphen
##  --the "WeBWorK element" that was accessed
##  --the "runTime" required to process the problem
##
##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the timing_log.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values. 


## Load pandas and read in the data set
import pandas as pd # load pandas as pd
import numpy as np # load numpy as np

loglines = pd.Series(open('timing_log.txt').read().splitlines())


## 1.  How many log entries were for requests for a PDF version of an
##     assignment?  Those are indicated by "hardcopy" appearing in the 
##     WeBWorK element.

# check which logs contain 'hardcopy' and count them
q1 = loglines.str.contains('hardcopy').sum() # number of log entries requesting a PDF


## 2.  What percentage of log entries involved a Spring '12 section of MATH 1320?

# find proportions of values that contain 'Spring12-MATH1320', subset True
# and multiply by 100
q2 = 100 * loglines.str.contains('Spring12-MATH1320').value_counts(normalize=True)[True]  # percentage of log entries, Spring '12 MATH 1320


## 3. How many different classes use the system? Treat each different name 
##    as a different class, even if there is more than one section of a course.  

# regex to match class names
class_name = r'/webwork2/([^\s/]+)[/\]]'
# extract class names from logs
class_chunk = loglines.str.extract(class_name).iloc[:,0]
# find unique names and find the size
q3 = class_chunk.unique()[pd.Series(class_chunk.unique()).notna()].size  # number of different classes using the system
                        

## 4.  Find the percentage of log entries that came from an initial
##     log in.  For those, the WeBWorK element has the form
##
##          [/webwork2/ClassName] or [/webwork2/ClassName/]
##
##     where "ClassName" is the name of a class.   

# regex to match initial logins
init_login = r'/webwork2/[^/\s]+/?\]'
# find proportions of values that match init_login, subset True and multiply
# by 100
q4 = 100 * loglines.str.contains(init_login).value_counts(normalize=True)[True]  # percentage of log entries from initial log in


## 5.  Determine the percentage of log entries for each section of MATH 1310
##     from Spring 2012, among the total number of log entries for MATH 1310,
##     Spring 2012.  Give the percentages as a Series with class name as
##     index and percentages as values, sorted by percentage largest to smallest.
##     (The class name should be of the form 'Spring12-MATH1310-InstructorName')

# regex to match sections of MATH 1320 from Spring 2012
section = r'Spring12-MATH1310-(\w+)'
# subset logs which match
math1310_sp12 = loglines.loc[loglines.str.contains('Spring12-MATH1310')]
# find proportions of values with each section, multiply by 100
q5 = 100 * math1310_sp12.str.extract(class_name).iloc[:,0].value_counts(normalize=True)  # Series of MATH 1310 sections and percentage within MATH 1310


## 6.  How many log entries were from instructors performing administrative
##     tasks?  Those are indicated by "instructor" alone in the 3rd position of
##     the WeBWorK element.  

# subset loglines where instructor is the 3rd element, count
q6 = loglines.loc[loglines.str.split('/').str[3] == 'instructor'].size  # number of instructor administrative log entries


## 7.  Find the number of log entries for each hour of the day. Give the
##     counts for the top-5 (plus ties as usual) as a Series, with hour of day
##     as index and the count as values, sorted by count from largest to 
##     smallest.

# regex to find hours
hour = r'(\d{2}):\d{2}:\d{2}'
# extract hours, count values, subset 5 largest, including ties
q7 = loglines.str.extract(hour).value_counts().nlargest(5, keep='all')  # Series of entry count by hour, top 5


## 8.  Find the number of log entries for each minute of each hour of the day. 
##     Give the counts for the top-8 (plus ties as usual) as a Series, with 
##     hour:minute pairs as index and the count as values, sorted by count 
##     from largest to smallest.  (An example of a possible index entry
##     is 15:47)

#regex to find hour and minute combinations
hour_minute = r'(\d{2}:\d{2}):\d{2}'
# extract hour and minute combinations, count values, subset 8 largest, including ties
q8 = loglines.str.extract(hour_minute).value_counts().nlargest(8, keep='all')  # Series of counts by hour:minute, top-8 plus ties


## 9. Determine which 5 classes had the largest average "runTime".  Give a 
##    Series of the classes and their average runTime, with class as index
##    and average runTime as value, sorted by value from largest to smallest.

# regex to find runtimes
run_time = r'runTime = (\d+\.\d+) sec'
# create DataFrame with class name and runtime
some_data = pd.DataFrame({
    'class': loglines.str.extract(class_name).iloc[:,0],
    'runTime': loglines.str.extract(run_time).iloc[:,0].astype(float)
})
# group by class name, take means, subset runTime, subset 5 largest, including ties 
q9 = some_data.groupby('class').mean()['runTime'].nlargest(5, keep='all')  # Series of classes and average runTimes


## 10. Determine the percentage of log entries that were accessing a problem.  
##     For those, the WeBWorK element has the form
##
##           [/webwork2/ClassName/AssignmentName/Digit]
##     or
##           [/webwork2/ClassName/AssignmentName/Digit/]
##
##     where "ClassName" is the name of the class, "AssignmentName" the
##     name of the assignment, and "Digit" is a positive digit.

# regex to find problem accesses
problem = r'/webwork2/([^\s/]+/[^\s/]+/\d+)[/]?]'
# find proportion that matches problem and multiply by 100
q10 = 100 * loglines.str.contains(problem).value_counts(normalize=True)[True]  # percentage of log entries accessing a problem
 

## 11. Find the top-10 (plus tied) WeBWorK problems that had the most log entries,
##     and the number of entries for each (plus ties as usual).  Sort the 
##     table from largest to smallest.
##     (Note: The same problem number from different assignments and/or
##     different classes represent different WeBWorK problems.) 
##     Give your answer as a Series with index entries of the form
##
##          ClassName/AssignmentName/Digit
##
##     and counts for values, sorted by counts from largest to smallest.

# extract problem names, count values, subset 0 largest, including ties
q11 = loglines.str.extract(problem).iloc[:,0].value_counts().nlargest(10, keep='all')  # Series of problems and counts

