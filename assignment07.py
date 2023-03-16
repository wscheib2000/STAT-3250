##
## File: assignment07.py (STAT 3250)
## Topic: Assignment 7 
##

##  This assignment requires the data file 'movies.txt'.  This file
##  contains records for nearly 3900 movies, including a movie ID number, 
##  the title (with year of release, which is not part of the title), and a 
##  list of movie genre classifications (such as Romance, Comedy, etc).  Note
##  that a given movie can be classified into more than one genre -- for
##  instance Toy Story is classified as "Animation", "Children's", and 
##  "Comedy".

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

# Read in the movie data as text; leave in encoding = 'utf8'
# create data frame
movielines = pd.read_csv('movies.txt', encoding = 'utf8',  delimiter='::', header=None)
movies = pd.DataFrame({
    'Title': movielines[1].str[:-7],
    'Year': movielines[1].str[-5:-1].astype(int),
    'Genre': movielines[2]
})
movies['Title'] = movies['Title'].str.strip()
movies['Genre'] = movies['Genre'].str.strip()


## 1.  Determine the number of movies included in genre "Animation", the number
##     in genre "Horror", and the number in both "Comedy" and "Crime".

# sum number of movies which have Animation in their Genre
q1a = movies['Genre'].str.contains('Animation').sum()  # Genre includes Animation
# sum number of movies which have Horror in their Genre
q1b = movies['Genre'].str.contains('Horror').sum()  # Genre includes Horror
# sum number of movies which have both Comedy and Crime in their Genre
comedy_and_crime = movies.loc[movies['Genre'].str.contains('Comedy') & movies['Genre'].str.contains('Crime'),:]
q1c = comedy_and_crime.loc[:,'Title'].size  # Genre includes both Comedy and Crime


## 2.  Among the movies in the genre "Horror", what percentage have the word
##     "massacre" in the title?  What percentage have 'Texas'? (Upper or lower
##     cases are allowed here.) 

# subset horror movies
horror = movies.loc[movies['Genre'].str.contains('Horror'),:]
# sum horror movies that contain 'massacre' in the title
num2a = horror['Title'].str.lower().str.contains('massacre').sum()
# divide by total number of horror movies and multiply by 100
q2a = 100 * num2a / horror['Title'].size  # percentage in Horror that includes 'massacre'
# sum horror movies that contain 'texas' in the title
num2b = horror['Title'].str.lower().str.contains('texas').sum()
# divide by total number of horror movies and multiply by 100
q2b = 100 * num2b / horror['Title'].size  # percentage in Horror that includes 'texas'


## 3.  Among the movies with exactly one genre, determine the genres that
##     have at least 50 movies classified with that genre.  Give a Series 
##     with genre as index and counts as values, sorted largest to smallest 
##     by count.

# subset movies where the Genre does not contain |, group by genre, and count
one_genre_counts = movies.loc[~movies['Genre'].str.contains('\|'),:].groupby('Genre').count()['Title']
# subset genres with at least 50 movies
q3 = one_genre_counts.sort_values(ascending=False).loc[one_genre_counts >= 50]  # Series of genres for at least 50 movies and counts


## 4.  Determine the number of movies that have 1 genre, 2 genres, 3 genres, 
##     and so on.  Give your results in a Series, with the number of genres
##     as the index and the counts as values, sorted by index values from
##     smallest to largest. 

# create n_Genre column with number of |'s in the Genre + 1
movies['n_Genre'] = movies['Genre'].str.count('\|')+1
# group by n_Genre, count, and sort by the index
q4 = movies.groupby('n_Genre').count()['Title'].sort_index()  # Series of number of genres and counts


## 5.  How many remakes are in the data? We say a movie is a remake if the title is
##     exactly the same as the title of an older movie. For instance, if 'Hamlet'  
##     is in the data set 4 times, then 3 of those should be counted as remakes.
##     (Note that a sequel is not the same as a remake -- "Jaws 2" is completely
##     different from "Jaws".)

# group by title and count
title_counts = movies.groupby(movies['Title']).count()['Genre']
# one of each title is not a remake, so subract 1 from them all and sum to get total remakes
q5 = (title_counts - 1).sum()  # number of remakes in data set


## 6.  Determine for each genre the percentage of movies in the data set that
##     are classified as that genre.  Give a Series of all with 8% or more,
##     with genre as index and percentage as values, sorted from highest to 
##     lowest percentage. 

# count total number of appearances of each genre
genre_counts = movies['Genre'].str.split('\|', expand=True).unstack().value_counts()
# divide by total number of movies and multiply by 100
genre_pcts = 100*genre_counts/movies['Title'].size
# sort and select all with 8% or more
q6 = genre_pcts.sort_values(ascending=False).loc[genre_pcts >= 8]  # Series of genres and percentages


## 7.  It is thought that musicals have become less popular over time.  We 
##     judge that assertion here as follows: Compute the median release year 
##     for all movies that have genre "Musical", and then do the same for all
##     other movies.  

# subset Year, group by if the genre contains Musical, calculate medians
median_years = movies['Year'].groupby(movies['Genre'].str.contains('Musical')).median()
# subset true and false
q7a = median_years[True]  # median release year for Musical
q7b = median_years[False]  # median release year for non-Musical 


##  8. Determine how many movies came from each decade in the data set.
##     An example of a decade: The years 1980-1989, which we would label as
##     1980.  (Use this convention for all decades in the data set.) 
##     Give your answer as a Series with decade as index and counts as values,
##     sorted by decade 2000, 1990, 1980, ....

# create decade column
movies['Decade'] = movies['Year'] // 10 * 10
# group by decade, count, sort
q8 = movies.groupby('Decade').count()['Title'].sort_index(ascending=False)  # Series of decades and counts


##  9. For each decade in the data set, determine the percentage of titles
##     that have exactly one word.  (Note: "Jaws" is one word, "Jaws 2" is not)
##     Give your answer as a Series with decade as index and percentages as values,
##     sorted by decade 2000, 1990, 1980, ....

# create One_word column (T if title is 1 word, F otherwise)
movies['One_word'] = movies['Title'].str.count(' ') == 0
# group by decade, calculate proportions, multiply by 100
counts = 100 * movies.groupby('Decade')['One_word'].value_counts(normalize=True)
# subset false, do 100-value to get true, sort, return to single index
q9 = (100-counts.loc[counts.index.get_level_values('One_word')==False]).sort_index(ascending=False).reset_index(level = 'One_word', drop=True)  # Series of percentage 1-word titles by decade


## 10. For each genre, determine the percentage of movies classified in
##     that genre also classified in at least one other genre.  Give your 
##     answer as a Series with genre as index and percentages as values, 
##     sorted largest to smallest percentage.

# create data frame with list of genres as one column and column which is T if
# there is more than 1 genre, F otherwise as the other, explode by genre (results
# in a dataframe with genres in the first column and number of genres in the movie
# it came from in the second)
d10 = pd.DataFrame({
    'Genre': movies['Genre'].str.split('\|'),
    'MultGenre': movies['Genre'].str.split('\|').str.len() > 1
}).explode('Genre')
# group by genre, calculate proportions, multiply by 100
counts10 = d10.groupby('Genre')['MultGenre'].value_counts(normalize=True) * 100
# subset true, sort, return to single index
q10 = counts10.loc[counts10.index.get_level_values('MultGenre')].sort_values(ascending=False).reset_index(level = 'MultGenre', drop=True)  # Series of genres, percentages
   

