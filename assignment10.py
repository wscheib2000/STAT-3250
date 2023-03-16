##
## File: assignment10.py (STAT 3250)
## Topic: Assignment 10 
##

##  For this assignment you will be working with Twitter data related
##  to the season opening of Game of Thrones on April 14, 2019.  You will use 
##  a set of over 10,000 tweets for this purpose.  The data is in the file 
##  'GoTtweets.txt'.  

##  Note: On this assignment it makes sense to use loops to extract 
##  information from the tweets. Go wild.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the GoTtweets.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  
 
import pandas as pd
import numpy as np

# read json data
tweets = pd.read_json('GoTtweets.txt', lines=True)

## 1.  The tweets were downloaded in several groups at about the same time.
##     Are there any that appear in the file more than once?  Give a Series 
##     with the tweet ID for any repeated tweets as the index and the number 
##     of times each ID appears in the file as values.  Sort by the index from
##     smallest to largest.

# value_counts on id column
t1 = tweets['id'].value_counts().sort_index()
# subset ids that appear > 1 times, sort index
q1 = t1[t1 > 1].sort_index() # Series of tweet IDs that appear > 1 time


## Note: For the remaining questions in this assignment, do not worry about 
##       any duplicate tweets.  Just answer the questions based on the 
##       existing data set.
    

## 2.  Determine the number of tweets that include 'Daenerys' (any combination
##     of upper and lower case; part of another work OK) in the text of the 
##     tweet.  Then do the same for 'Snow'.

# subset tweets where the text (converted to lowercase) contains the word,
# get number of rows
q2a = tweets.loc[tweets['text'].str.lower().str.contains('daenerys'),'id'].size  # number of tweets including 'daenerys'
q2b = tweets.loc[tweets['text'].str.lower().str.contains('snow'),'id'].size  # number of tweets including 'snow'


## 3.  Find the average number of hashtags included in the tweets. (You may get 
##     the wrong answer if you use the text of the tweets instead of the
##     hashtag lists.)

# transform the entities column into the length of the hashtags list for each row
tweets['n_hashtags'] = tweets['entities'].transform(lambda x: len(x['hashtags']))
# calculate mean of n_hashtags
q3 = tweets['n_hashtags'].mean()  # average number of hashtags per tweet

 
## 4.  Determine the tweets that have 0 hashtags, 1 hashtag, 2 hashtags,
##     and so on.  Give your answer as a Series with the number of hashtags
##     as index (sorted smallest to largest) and the corresponding number of
##     tweets as values. Include in your Series index only number of hashtags  
##     that occur for at least one tweet. (Note: See warning in #3)

# value_counts on n_hashtags
q4 = tweets['n_hashtags'].value_counts().sort_index()  # Series of number of hashtags and counts


## 5.  Determine the number of tweets that include the hashtag '#GoT', then
##     repeat for '#GameofThrones'.  (You may get the wrong answer if you
##     use the text of the tweets instead of the hashtag lists.)
##     Note: Hashtags are not case sensitive, so any of '#GOT', '#got', 'GOt' 
##     etc are all considered matches.

def contains_hashtag(x, hashtag_regex):
    if x['hashtags'] == []:
        return False
    else:
        # extract text from hashtags, convert to lowercase and check for hashtag, sum booleans, convert to Boolean
        return pd.Series(x['hashtags']).transform(lambda y: y['text']).str.lower().str.contains(hashtag_regex).sum() > 0

# transform entities column into count of hashtags which match the desired one
# using function above, sum
q5a = tweets['entities'].transform(lambda x: contains_hashtag(x, r'^got$')).sum()
q5b = tweets['entities'].transform(lambda x: contains_hashtag(x, r'^gameofthrones$')).sum()  # number of tweets with '#GameofThrones' hashtags and upper/lower variants             


## 6.  Some tweeters like to tweet a lot.  Find the screen name for all 
##     tweeters with at least 3 tweets in this data.  Give a Series with 
##     the screen name (in lower case) as index and the number of tweets as 
##     value, sorting by the index in alphbetical order.  

# transform user column into lowercase version of screen_name, value_counts
t6 = tweets['user'].transform(lambda x: x['screen_name'].lower()).value_counts()
# subset at least 3, sort index
q6 = t6[t6 >= 3].sort_index()  # Series of screen name and counts

    
## 7.  Among the screen names with 3 or more tweets, find the average
##     'followers_count' for each and then give a table with the screen  
##     and average number of followers.  (Note that the number of
##     followers might change from tweet to tweet.)  Give a Series with
##     screen name (in lower case) as index and the average number of followers  
##     as value, sorting by the index in alphbetical order.  

# json_normalize to extract data from user column
d7 = pd.json_normalize(tweets['user'])
# make screen_name lowercase
d7['screen_name'] = d7['screen_name'].str.lower()
# subset rows where screen_name is in q6's index, groupby screen_name,
# calculate mean follower count, sort index
q7 = d7.loc[d7['screen_name'].isin(q6.index),:].groupby('screen_name')['followers_count'].mean().sort_index()  # Series of screen names and mean follower counts  

                                                                
## 8.  Determine the hashtags that appeared in at least 50 tweets.  Give
##     a Series with the hashtags (lower case) as index and the corresponding 
##     number of tweets as values, sorted alphabetically by hashtag.

# transform entities column into a list of lowercased text values for all hashtags,
# get unique values, explode, value_counts
t8 = tweets['entities'].transform(lambda x: [] if x['hashtags'] == [] else [y['text'].lower() for y in x['hashtags']]).transform(lambda z: np.unique(np.array(z))).explode('entities').value_counts()
# subset values >= 50, sort index
q8 = t8[t8 >= 50].sort_index()  # Series of hashtags and counts
        

##  9.  Some of the tweets include the location of the tweeter.  Give a Series
##      of the names of countries with at least three tweets, with country 
##      name as index and corresponding tweet count as values.  Sort the
##      Series alphabetically by country name.

# create country column by transforming place column, nan if there is no place,
# country name otherwise
tweets['country'] = tweets['place'].transform(lambda x: np.nan if x is None else x['country'])
# value_counts
t9 = tweets['country'].value_counts()
# subset values >= 3, sort index
q9 = t9[t9 >= 3].sort_index()   # Series of countries with at least three tweets


## Questions 10-11: The remaining questions should be done using regular 
##                  expressions as described in the class lectures.

## 10.  Determine the percentage of tweets (if any) with a sequence of 3 or more
##      consecutive digits.  (No spaces between the digits!)  For such tweets,
##      apply 'split()' to create a list of substrings.  Among all the 
##      substrings with a sequence of at least three consecutive digits,
##      determine the percentage where the substring starts with a '@' at the 
##      beginning of the substring.

# create column true if there are three or more consecutive digits, false if not
tweets['three_consec_dig'] = tweets['text'].str.contains(r'\d{3,}')
# value_counts with normalize = True, subset True, multiply by 100
q10a = 100 * tweets['three_consec_dig'].value_counts(normalize=True)[True]  # percentage of tweets with three consecutive digits
# split text on whitespace and explode
d10b1 = tweets['text'].str.split().explode('text')
# subset where there are three or more consecutive digits
d10b2 = d10b1.loc[d10b1.str.contains(r'\d{3,}')]
# 100 * number that start with @ over total number
q10b = 100 * d10b2.str.contains(r'^@').sum() / d10b2.size  # percentage starting with @ among substrings with 3 consec digits


## 11.  Determine if there are any cases of a tweet with a 'hashtag' that is
##      actually not a hashtag because there is a character (letter or digit)
##      immediately before the "#".  An example would be 'nota#hashtag'.
##      Count the number of tweets with such an incorrect 'hashtag'.

# check whether text contains a letter or digit followed by a hashtag, sum booleans
q11 = tweets['text'].str.contains(r'[A-Za-z0-9]#').sum()  # count of tweets with bad hashtag




