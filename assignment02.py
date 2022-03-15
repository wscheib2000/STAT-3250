##
## File: assignment02.py (STAT 3250)
## Topic: Assignment 2
##

import numpy as np

## Two *very* important rules that must be followed in order for your 
## assignment to be graded correctly:
##
## a) The file name must be exactly "assignment02.py" (without the quotes)
## b) The variable names followed by "= None" must not be changed and these 
##    names variable names should not be used anywhere else in your file.  Do   
##    not delete these variables, if you don't know how to find a value just  
##    leave it as is. (If a variable is missing the autograder will not grade  
##    any of your assignment.)


## Questions 1-7: For the questions in this part, use the following
##  lists as needed:
    
list01 = [5, -9, -1, 8, 0, -1, -2, -7, -1, 0, -1, 6, 7, -2, -1, -5]
list02 = [-2, -5, -2, 8, 7, -7, -11, 1, -1, 6, 6, -7, -9, 1, 5, -11]
list03 = [9, 0, -8, 3, 2, 9, 3, -4, 5, -9, -7, -3, -11, -6, -5, 1]
list04 = [-4, -6, 8, 8, -5, -5, -11, -3, -1, 7, 0, 2, -5, -2, 0, -5]
list05 = [-11, -3, 8, -9, 2, -8, -7, -12, 7, 3, 2, 0, 6, 4, -11, 6]
biglist = list01 + list02 + list03 + list04 + list05

## Questions 1-7: Use for loops to answer each of the following applied  
##  to the lists defined above.
 
## 1.  Add up the squares of the entries of biglist.

s1 = 0
for i in biglist:
    s1 += i**2
q1 = s1
# q1 = [i**2 for i in biglist] <- sad I can't use this yet :(


## 2.  Create "newlist01", which has 14 entries, each the sum of the 
##      corresponding entry from list01 added to the corresponding entry
##      from list02.  That is,
##     
##         newlist01[i] = list01[i] + list02[i] 
##
##      for each 0 <= i <= 13.

newlist01 = [0] * 14
for i in range(14):
    newlist01[i] = list01[i] + list02[i]
q2 = newlist01


## 3.  Determine the number of entries in biglist that are less than 6.

ct3 = 0
for i in biglist:
    if i < 6:
        ct3 += 1
q3 = ct3


## 4.  Create a new list called "newlist02" that contains the elements of
##      biglist that are greater than 5, given in the same order as the
##      elements appear in biglist.

newlist02 = []
for i in biglist:
    if i > 5:
        newlist02.append(i)
q4 = newlist02


## 5.  Find the sum of the positive entries of biglist.

s5 = 0
for i in biglist:
    if i > 0:
        s5 += i
q5 = s5


## 6.  Make a list of the first 19 negative entries of biglist, given in
##      the order that the values appear in biglist.

neglist = [0] * 19
l = 0 #number of non-zero values in the list, incremented when value is added
for i in biglist:
    if i < 0:
        neglist[l] = i
        l += 1 #increment non-zero value counter
    if l == 19:
        break
q6 = neglist
  
      
##  7. Identify all elements of biglist that have a smaller element that 
##      immediately preceeds it.  Make a list of these elements given in
##      the same order that the elements appear in biglist.

l7 = []
for i in range(len(biglist)):
    if i < len(biglist)-1 and biglist[i] < biglist[i+1]:
        l7.append(biglist[i+1])
q7 = l7


## Questions 8-9: These questions use simulation to estimate probabilities
##  and expected values.  

##  8. Consider the following game: You flip a fair coin.  If it comes up
##      tails, then you win $1.  If it comes up heads, then you get to 
##      simultaneously flip four more fair coins.  In this case you win $1 
##      for each head that appears on all flips, plus you get an extra $7 if 
##      all five flips are heads.
##
##      Use 100,000 simulations to estimate the average amount of money won 
##      when playing this game.

win = [0] * 100000
for i in range(100000):
    if np.random.choice([0,1], 1)[0] == 0:
        win[i] = 1
    else:
        win[i] = 1 + np.sum(np.random.choice([0,1], 4)) # first heads + number of heads in next 4 flips
        if win[i] == 5:
            win[i] += 7
q8 = np.mean(win)


##  9. Jay is taking a 15 question true/false quiz online.  The
##      quiz is configured to tell him whether he gets a question
##      correct before proceeding to the next question.  The 
##      responses influence Jay's confidence level and hence his 
##      exam performance.  In this problem we will use simulation
##      to estimate Jay's average score based on a simple model.
##      We make the following assumptions:
##    
##      * At the start of the quiz there is a 81% chance that 
##        Jay will answer the first question correctly.
##      * For all questions after the first one, if Jay got 
##        the previous question correct, then there is a
##        90% chance that he will get the next question
##        correct.  (And a 10% chance he gets it wrong.)
##      * For all questions after the first one, if Jay got
##        the previous question wrong, then there is a
##        72% chance that he will get the next question
##        correct.  (And a 28% chance he gets it wrong.)
##      * Each correct answer is worth 5 points, incorrect = 0.
##
##      Use 100,000 simulated quizzes to estimate Jay's average 
##      score.

scores = [0] * 100000
for i in range(100000):
    score = 0
    prob = 0.81
    for j in range(15): #each quiz has 15 questions
        result = np.random.choice([5,0], 1, p=[prob, 1-prob])[0]
        score += result
        prob = 0.90 if result else 0.72 #0.90 if he got the question right, 0.72 otherwise
    scores[i] = score
q9 = np.mean(scores)



