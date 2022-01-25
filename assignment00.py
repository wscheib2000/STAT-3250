##
## Assignment 00, STAT 3250
##

## This assignment is for practice only, the score will not be used.

## Two *very* important rules that must be followed in order for your assignment
## to be graded correctly:
##
## a) The file name must be exactly "assignment00.py" (without the quotes)
## b) The variable names followed by "= None" must not be changed and these names
##    should not be used anywhere else in your file.  Do not delete these 
##    variables, if you don't know how to find a value just leave it as is.
##    (If a variable is missing the autograder will not grade any of your
##    assignment.)

## When you answer each question, replace the "None" to the right of the equals
## sign with code or the correct value.

## Question 1
##
## Find the sum of 23 and 119

q1 = 23 + 119

## Question 2
##
## Create a list with "Hello" as the first element and "World" as the second element.

q2 = ["Hello", "World"]

## Question 3
##
## Determine the first 5 prime numbers, in order.  Then give: 
##   (a) the largest of these 
##   (b) a list of the 1st, 2nd, and 4th of these (when small to large)
##   (c) a list of all 5 (smallest to largest)

## 3(a)

primes = [5,7,11,2,3]

q3a = max(primes)

## 3(b)
primes.sort()
q3b = primes[:2] + [primes[3]]

## 3(c)
q3c = primes
