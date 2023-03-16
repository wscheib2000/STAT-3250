##
## File: assignment08.py (STAT 3250)
## Topic: Assignment 8 
##

##  This assignment requires data from three files: 
##
##      'movies.txt':  A file of nearly 3900 movies
##      'reviewers.txt':  A file of over 6000 reviewers who provided ratings
##      'ratings.txt':  A file of over 1,000,000 movie ratings
##
##  The file 'readme.txt' has more information about these files.
##  You will need to consult the readme.txt file to answer some of the questions.

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

import pandas as pd

## It is recommended that you read in the data sets in the manner shown below.
# read in data, specifying types for consistency
movies = pd.read_csv('movies.txt', delimiter='::', names=['MovieID', 'Title', 'Genres'],  dtype={'MovieID': 'int64', 'Title': 'str', 'Genres': 'str'})
reviewers = pd.read_csv('reviewers.txt', delimiter='::', names=['ReviewerID', 'Gender', 'Age', 'Occupation', 'Zip-code', 'State'],  dtype={'ReviewerID': 'int64', 'Gender': 'str', 'Age': 'int64', 'Occupation': 'int64', 'Zip-code': 'str', 'State': 'str'})
ratings = pd.read_csv('ratings.txt', delimiter='::', names=['ReviewerID', 'MovieID', 'Rating', 'Timestamp'],  dtype={'ReviewerID': 'int64', 'MovieID': 'int64', 'Rating': 'int64'}, parse_dates=['Timestamp'], date_parser=lambda x: pd.to_datetime(x, unit='s'))

## 1.  Based on the data in 'reviewers.txt': Determine the percentage of all 
##     reviewers that are female.  Determine the percentage of all reviewers in
##     the 35-44 age group.  Among the 18-24 age group, find the percentage 
##     of reviewers that are male.

# value_counts gender column, subset female, multiply by 100
q1a = 100 * reviewers['Gender'].value_counts(normalize=True)['F']  # percentage of female reviewers
# value_counts age column, subset 35, multiply by 100
q1b = 100 * reviewers['Age'].value_counts(normalize=True)[35]  # percentage age 35-44
# subset 18-24, value_counts gender column, subset male, multiply by 100
q1c = 100 * reviewers.loc[reviewers['Age'] == 18, 'Gender'].value_counts(normalize=True)['M']  # percentage of males reviewers in 18-24 age group


## 2.  Give a year-by-year Series of counts for the number of ratings, with
##     the rating year as index and the counts as values, sorted by rating
##     year in ascending order.

# group by year, count, subset rating column
q2 = ratings.groupby(ratings['Timestamp'].dt.year).count()['Rating']  # Series of rating counts by year rated


## 3.  Determine the average rating from female reviewers and the average  
##     rating from male reviewers.

# merge reviewers and ratings
d3 = pd.merge(reviewers, ratings)
# group by gender, subset rating column, calculate means
t3 = d3.groupby('Gender')['Rating'].mean()
# subset female
q3a = t3['F']  # average rating for female reviewers
# subset male
q3b = t3['M']  # average rating for male reviewers


## 4.  Determine the number of movies that received an average rating of 
##     less than 1.75.  (Movies and remakes should be considered as
##     different.)

# merge ratings and movies
d4 = pd.merge(ratings, movies)
# group by title, subset rating column, calculate means
t4 = d4.groupby('Title')['Rating'].mean()
# select means less than 1.75, get number of entries
q4 = t4.loc[t4 < 1.75].size  # count of number with average rating less than 1.75


## 5.  Determine the number of movies listed in 'movies.txt' for which there
##     is no rating in 'ratings.txt'.  

# merge movies and ratings, keeping all entries from movies
d5 = pd.merge(movies, ratings, how='left')
# subset where rating is na, get nunmber of entries
q5 = d5.loc[d5['Rating'].isna(), 'Title'].size  # number of movies that were not rated


## 6.  Among the ratings from male reviewers, determine the average  
##     rating for each occupation classification (including 'other or not 
##     specified'), and give the results in a Series sorted from highest to 
##     lowest average with the occupation title (not the code) as index.

# merge ratings and male reviewers
d6 = pd.merge(ratings, reviewers.loc[reviewers['Gender'] == 'M', :])
# declare mapping dictionary
occupations = {
    0: 'other or not specified',
	1: 'academic/educator',
	2: 'artist',
	3: 'clerical/admin',
	4: 'college/grad student',
	5: 'customer service',
	6: 'doctor/health care',
	7: 'executive/managerial',
	8: 'farmer',
	9: 'homemaker',
	10: 'K-12 student',
	11: 'lawyer',
	12: 'programmer',
	13: 'retired',
	14: 'sales/marketing',
	15: 'scientist',
	16: 'self-employed',
	17: 'technician/engineer',
	18: 'tradesman/craftsman',
	19: 'unemployed',
	20: 'writer'
}
# use mapping dictionary to transform occupation column, making use of lambda function
d6['Occupation'] = d6['Occupation'].transform(lambda x: occupations[x])
# group by occupation, subset rating column, calculate means, sort values
q6 = d6.groupby('Occupation')['Rating'].mean().sort_values(ascending=False)  # Series of average ratings by occupation


## 7.  Determine the average rating for each genre, and give the results in
##     a Series with genre as index and average rating as values, sorted 
##     alphabetically by genre.

# merge movies and ratings
d7a = pd.merge(movies, ratings)
# create data frame with list of genres as Genre and rating as Rating and explode
# on Genre to end up with a data frame with Genre and Rating columns
d7b = pd.DataFrame({
    'Genre': d7a['Genres'].str.split('\|'),
    'Rating': d7a['Rating']
}).explode('Genre')
# group by genre, subset rating, calculate means
q7 = d7b.groupby('Genre')['Rating'].mean()  # Series of average rating by genre   


## 8.  For the reviewer age category, assume that the reviewer has age at the 
##     midpoint of the given range.  (For instance '35-44' has age (35+44)/2 = 39.5)
##     For 'under 18' assume an age of 16, and for '56+' assume an age of 60.
##     For each possible rating (1-5) determine the average age of the reviewers
##     giving that rating.  Give your answer as a Series with rating as index
##     and average age as values, sorted by rating from 1 to 5.

# merge ratings, reviewers
d8 = pd.merge(ratings, reviewers)
# declare mapping dictionary
age_dict = {
    1: 16,
	18: (18+24)/2,
	25: (25+34)/2,
	35: (35+44)/2,
	45: (45+49)/2,
	50: (50+55)/2,
	56: 60  
}
# use mapping dictionary to transform age column, making use of lambda function
d8['Age'] = d8['Age'].transform(lambda x: age_dict[x])
# group by rating, subset age, calculate means
q8 = d8.groupby('Rating')['Age'].mean()  # Series of average age by rating


## 9.  Find the top-5 'states' in terms of average rating.  Give as a Series
##     with the state as index and average rating as values, sorted from 
##     highest to lowest average rating. (Include any ties as usual)
##     Note: 'states' includes US territories and military bases. See the 
##     readme.txt file for more information on what constitutes a 'state'
##     for this assignment.

# merge ratings, reviewers
d9 = pd.merge(ratings, reviewers)
# group by state, subet rating, calculate means, take 5 largest including ties
q9 = d9.groupby('State')['Rating'].mean().nlargest(5, keep='all')  # top-5 states by average rating


## 10. For each age group, determine the occupation that gave the lowest 
##     average rating.  Give a Series that includes the age group code and 
##     occupation title as a multiindex, and average rating as values.  Sort  
##     the Series by age group code from youngest to oldest. 

# mearge ratings and reviewers
d10 = pd.merge(ratings, reviewers)
# use mapping dictionary to transform occupation column, making use of lambda function
d10['Occupation'] = d10['Occupation'].transform(lambda x: occupations[x])
# group by age and occupation, subset rating, calculate means, group by age without
# duplicating keys, take smallest value
q10 = d10.groupby(['Age','Occupation'])['Rating'].mean().groupby('Age', group_keys=False).nsmallest(1)  # Series of average ratings by age code and occupation title




