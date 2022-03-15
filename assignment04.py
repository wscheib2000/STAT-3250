##
## File: assignment04.py (STAT 3250)
## Topic: Assignment 4
##

##  This assignment requires the data file 'airline_tweets.csv'.  This file
##  contains records of over 14000 tweets and associated information related
##  to a number of airlines.  You should be able to read this file in using
##  the usual pandas methods.

##  Gradescope will review your code using a version of airline_tweets.csv
##  that has had about 50% of the records removed.  You will need to write
##  your code in such a way that your file will automatically produce the
##  correct answers on the new set of data.  

import pandas as pd # load pandas as pd
import numpy as np  # load numpy as np

air = pd.read_csv('airline_tweets.csv')  # Read in the data set
temp = air.loc[0:10,:]
## Questions 1-8: These questions should be done without the use of loops.

## 1.  Determine the number of tweets for each airline, indicated by the
##      name in the 'airline' column of the data set.  Give the airline 
##      name and corresponding number of tweets as a Series with airline
##      name as the index, sorted by tweet count from most to least.
# subset airline column, group by it, count, and sort the values
tmp1 = air['airline'].groupby(air['airline'])
q1 = tmp1.count().sort_values(ascending=False)  # Series of airlines and number of tweets


## 2.  For each airline's tweets, determine the percentage that are positive,
##      based on the classification in 'airline_sentiment'.  Give the airline 
##      name and corresponding percentage as a Series with airline
##      name as the index, sorted by percentage from largest to smallest
# group those tweets with positive airline sentiment by airline, count, and
# compute percenages based on denominator of total tweets per airline. Sort
tmp2 = air.loc[air['airline_sentiment']=='positive',:].groupby(['airline'])['airline'].count()
q2 = 100*(tmp2 / air['airline'].groupby(air['airline']).count()).sort_values(ascending=False)  # Series of airlines and percentage of positive tweets


## 3.  Find all user names (in the 'name' column) with at least 25 tweets
##      along with the number of tweets for each.  Give the user names and
##      corresponding counts as a Series with user name as index, sorted
##      by count from largest to smallest
# group names by name, count, subset names with more than 25 tweets, sort
tmp3 = air['name'].groupby(air['name']).count().rename('count')
q3 = tmp3[tmp3.values >= 25].sort_values(ascending=False)  # Series of users with at least 25 tweets


## 4.  Determine the percentage of tweets from users who have more than five
##      tweets in this data set. (Note that this is not the same as the
##      percentage of users with more than five tweets.)
# Use code from last question, subset users with more tha 5 tweets, sum up the
# number of tweets, and divide by the total number of tweets
q4 = 100 * np.sum(tmp3.values[tmp3.values > 5]) / np.sum(tmp3.values)  # Percentage of tweets from users with more than 5 tweets                            
                               

## 5.  Among the negative tweets, determine the four reasons are the most common.
##      Give the percentage among all negative tweets for each as a Series 
##      with reason as index, sorted by percentage from most to least
tmp5 = air.loc[air['airline_sentiment'] == 'negative','negativereason']
q5 = (100*tmp5.groupby(air['negativereason']).count() / tmp5.count()).sort_values(ascending=False).iloc[:4]  # Series of reasons and percentages


## 6.  How many tweets include a link to a web site? (Indicated by the 
##      presence of "http" anywhere in the tweet.)

q6 = air.loc[air['text'].str.contains('http'),'text'].count()  # Number of tweets that include a link


## 7.  How many tweets include the word "air" (upper or lower case,
##      not part of another word)?

q7 = air.loc[(" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s]+', ' ').str.contains(' air '), 'text'].count()  # Number of tweets that include 'air'


## 8.  How many times total does the word "help" appear in a tweet, either in
##      upper or lower case and not part of another word.

q8 = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s]+', ' ').str.count(' help ').sum()  # Number of times that 'help' is included


## Questions 9-13: Some of these questions can be done without the use of 
##  loops, while others cannot.  It is preferable to minimize the use of
##  loops where possible, so grading will reflect this.
##
##  Some of these questions involve hashtags and @'s.  These are special 
##  Twitter objects subject to special rules.  For these problems we assume
##  that a "legal" hashtag:
##
##  (a) Starts with the "#" (pound) symbol, followed by letter and/or numbers 
##       until either a space or punctuation mark (other than "#") is encountered.
##   
##      Example: "#It'sTheBest" produces the hashtag "#It"
##
##  (b) The "#" symbol can be immediately preceded by punctuation, which is 
##       ignored. If "#" is immediately preceded by a letter or number then
##       it is not a hashtag.
##
##      Examples: "The,#dog,is brown"  produces the hashtag "#dog"
##                "The#dog,is brown" does not produce a hashtag
##                "#dog1,#dog2" produces hashtags "#dog1" and "#dog2"
##                "#dog1#dog2" produces the hashtag "#dog1#dog2"
##
##  (c) Hashtags do not care about case, so "#DOG" is the same as "#dog"
##       which is the same as "#Dog".
##
##  (d) The symbol "#" by itself is not a hashtag
##
##  The same rules apply to Twitter handles (user names) that begin with the
##   "@" symbol.         

## 9.  How many of the tweets have at least two Twitter handles?
tmp9 = (" " + air['text'].str.lower()).str.replace(r'[^\w\s@]+', ' ').str.count(r'\s@\w+')
q9 = np.sum(tmp9 >= 2) # number of tweets with @ directed at a user besides the target airline


## 10. Suppose that a score of 3 is assigned to each positive tweet, 1 to
##      each neutral tweet, and -2 to each negative tweet.  Determine the
##      mean score for each airline and give the results as a Series with
##      airline name as the index, sorted by mean score from highest to lowest.
tmp10 = air['airline_sentiment'].groupby(air['airline']).value_counts().multiply(np.tile([-2, 1, 3], 6))
q10 = (tmp10.groupby('airline').sum()/air['airline'].value_counts()).sort_values(ascending=False)  # Series of airlines and mean scores 


## 11. What is the total number of hashtags in tweets associated with each
##      airline?  Give a Series with the airline name as index and the
##      corresponding totals for each, sorted from most to least.
tmp11 = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s#]+', ' ').str.count(r'\s#\w+')
q11 = tmp11.groupby(air['airline']).sum().sort_values(ascending=False)  # Series of airlines and hashtag counts


## 12. Among the tweets that "@" a user besides the indicated airline, 
##      find the percentage that include an "@" directed at the other  
##      airlines in this file. 
# isin
lookup_dict = {
    'Virgin America': '@virginamerica',
    'United': '@united',
    'Southwest': '@southwestair',
    'JetBlue': '@jetblue',
    'US Airways': '@usairways',
    'American': '@americanair'
}
tmp12 = air.loc[tmp9 >= 2,:].reset_index()
tmp12['text'] = (" " + tmp12['text'].str.lower() + ' ').str.replace(r'[^\w\s@]+', ' ')
num12, denom12 = 0, 0
for i in range(len(tmp12)):
    tmp12.loc[i, 'text'] = tmp12.loc[i, 'text'].replace(lookup_dict[tmp12.loc[i, 'airline']], ' ')
tmp12 = tmp12.loc[tmp12['text'].str.count(r'\s@\w+') > 0,:].reset_index()
for i in range(len(tmp12)):
    for handle in lookup_dict.values():
        if ' '+handle+' ' in tmp12.loc[i, 'text']:
            num12 +=1
            break
    denom12 += 1
        
q12 = 100 * num12 / denom12 # Percentage of tweets 


## 13. Suppose the same user has two or more tweets in a row, based on how they 
##      appear in the file. For such tweet sequences, determine the percentage
##      for which the most recent tweet (which comes nearest the top of the
##      file) is a positive tweet.
num13, denom13 = 0, 0
for i in range(len(air)-2, -1, -1):
    if air.loc[i, 'name'] == air.loc[i+1, 'name'] and (i == 0 or air.loc[i, 'name'] != air.loc[i-1, 'name']):
        if air.loc[i, 'airline_sentiment'] == 'positive':
            num13 += 1
        denom13 += 1
q13 = 100 * num13 / denom13  # Percentage of tweets


