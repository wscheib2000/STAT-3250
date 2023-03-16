##
## File: assignment12.py (STAT 3250)
## Topic: Assignment 12
##


##  In this assignment we revisit past NCAA men's basketball tournaments 
##  (including the glorious 2019 edition) using data from the file 
##
##      'ncaa.csv':  NCAA Men's Tournament Scores, 1985-2019
##
##  The organization of the file is fairly clear.  Each record has information
##  about one game, including the year, the teams, the final score, and each 
##  team's tournament seed.  

##  Two important points:
##    1) Each team is assigned a "seed" at the start of the tournament.  The
##       teams thought to be better are assigned smaller number seeds.  (So 
##       the best teams are assigned 1 and the worst assigned 16.)  In this 
##       assignment a "lower seed" refers to a worse team and hence larger 
##       seed number, with the opposite meaning for "higher seed". 
##    2) All questions refer only to the data in this in 'ncaa.csv' so you
##       don't need to worry about tournaments prior to 1985.

##  Note: The data set is from Data.World, with the addition of the 2019
##  tournament provided by your dedicated instructor. (There was no 2020
##  tournament and the 2021 tournament didn't turn out to your instructor's
##  liking so that data is omitted.)

##  Submission Instructions: Submit your code in Gradescope under 
##  'Assignment 12 Code'.  The autograder will evaluate your answers to
##  Questions 1-8.  You will also generate a separate PDF for the graphs
##  in Questions 9-11, to be submitted in Gradescope under 'Assignment 12 Graphs'.

import pandas as pd

df = pd.read_csv('ncaa.csv')

## 1.  Find all schools that have won the championship. Report your results in
##     a Series that has the schools as index and number of championships for
##     values, sorted alphabetically by school.

# use list comprehension to create Winner column based on scores
df['Winner'] = [team if score > score_1 else team_1 for score, team, team_1, score_1 in zip(df['Score'],df['Team'],df['Team.1'],df['Score.1'])]
# subset round 6, value counts, sort on index
q1 = df.loc[df['Round'] == 6,'Winner'].value_counts().sort_index()  # Series of champions and counts


## 2.  Determine all schools that have been in the tournament at least 25 times.
##     Report your results as a Series with schools as index and number of times
##     in the tournament as values, sorted alphabetically by school.

# concat series of all teams from both team columns, value counts
t2 = pd.concat([df.loc[df['Round'] == 1, 'Team'], df.loc[df['Round'] == 1, 'Team.1']]).value_counts()
# subset >= 25, sort index
q2 = t2[t2 >= 25].sort_index()  # Series of schools and tournament appearance counts


## 3.  Find all years when the school that won the tournament was seeded 
##     3 or lower. (Remember that "lower" seed means a bigger number!) Give  
##     a DataFrame with years as index and corresponding school and seed
##     as columns (from left to right).  Sort by year from least to most recent.

# use list comprehension to create Winning_Seed column based on scores 
df['Winning_Seed'] = [seed if score > score_1 else seed_1 for seed, score, score_1, seed_1 in zip(df['Seed'],df['Score'],df['Score.1'], df['Seed.1'])]
# subset round 6 (championship game), set the index to year
t3 = df.loc[df['Round'] == 6, ['Year', 'Winner', 'Winning_Seed']].set_index('Year')
# filter Winning_Seed >= 3
q3 = t3.loc[t3['Winning_Seed'] >= 3, :]  # DataFrame of years, schools, seeds


## 4.  Determine the average tournament seed for each school.  Make a Series
##     of all schools that have an average seed of 5.0 or higher (that is,
##     the average seed number is <= 5.0).  The Series should have schools
##     as index and average seeds as values, sorted alphabetically by
##     school

# concat all teams and seeds into one df
t4a = pd.concat([df.loc[df['Round'] == 1, ['Team', 'Seed']], df.loc[df['Round'] == 1, ['Team.1', 'Seed.1']].rename(columns={'Team.1': 'Team', 'Seed.1': 'Seed'})])
# group seed by team, calc means
t4b = t4a['Seed'].groupby(t4a['Team']).mean()
# subset <= 5, sort index
q4 = t4b[t4b <= 5].sort_index()  # Series of schools and average seed


## 5.  For each tournament round, determine the percentage of wins by the
##     higher seeded team. (Ignore games of teams with the same seed.)
##     Give a Series with round number as index and percentage of wins
##     by higher seed as values sorted by round in order 1, 2, ..., 6. 
##     (Remember, a higher seed means a lower seed number.)

# use list comprehension to create Losing_Seed column based on scores 
df['Losing_Seed'] = [seed if score < score_1 else seed_1 for seed, score, score_1, seed_1 in zip(df['Seed'],df['Score'],df['Score.1'], df['Seed.1'])]
# create Boolean Higher_Won column
df['Higher_Won'] = df['Winning_Seed'] < df['Losing_Seed']
# ignore games of teams with the same seed
d5 = df.loc[df['Seed'] != df['Seed.1'], :]
# group by round, subset Higher_Won, value counts with normalize,
# subset True from multiindex, multiply by 100
q5 = 100 * d5.groupby('Round')['Higher_Won'].value_counts(normalize=True).xs(True, level=1, drop_level=True)  # Series of round number and percentage higher seed wins


## 6.  For each seed 1, 2, 3, ..., 16, determine the average number of games
##     won per tournament by a team with that seed.  Give a Series with seed 
##     number as index and average number of wins as values, sorted by seed 
##     number 1, 2, 3, ..., 16. (Hint: There are 35 tournaments in the data set
##     and each tournamentstarts with 4 teams of each seed.  We are not 
##     including "play-in" games which are not part of the data set.)

# select columns
d6 = df.loc[:, ['Year', 'Winning_Seed']]
# group by Winning_Seed, subset Year, value counts, reindex all possible combs
# of seed and year to fill 0s
t6 = d6.groupby('Winning_Seed')['Year'].value_counts().reindex(pd.MultiIndex.from_product([range(1,17), df['Year'].unique()], names=['Winning_Seed', 'Year']), fill_value=0)
# group by Winning_Seed, dropping from index, calc means, divide by 4 to get
# average wins by a single team
q6 = t6.groupby('Winning_Seed', group_keys=False).mean() / 4  # Series of seed and average number of wins


## 7.  For each year's champion, determine their average margin of victory 
##     across all of their games in that year's tournament. Find the champions
##     that have an average margin of victory of at least 15. Give a DataFrame 
##     with year as index and champion and average margin of victory as columns
##     (from left to right), sorted by from highest to lowest average victory 
##     margin.

# calculate MOV column by subtracting one score from the other and making the
# result positive
df['MOV'] = (df['Score'] - df['Score.1']).transform(lambda x: x*-1 if x < 0 else x)
# find champions (subset round 6, Year and Winner columns)
champs = df.loc[df['Round'] == 6, ['Year', 'Winner']]
# select columns, group by year and winner, calculate means
avg_mov_by_team_and_year = df[['Year', 'Winner', 'MOV']].groupby(['Year', 'Winner']).mean()
# subset where index refers to a champion, reindex with just the year,
# sort dataframe by MOV descending
t7 = avg_mov_by_team_and_year.loc[avg_mov_by_team_and_year.index.isin(champs.values.tolist())].reset_index(level=1).sort_values(by='MOV', ascending=False)
q7 = t7.loc[t7['MOV'] >= 15,:]   # DataFrame of years, schools, average margin of victory


## 8.  Determine the 2019 champion.  Use code to extract the correct school,
##     not your knowledge of college backetball history.

# set index as year, subset Winner column, subset 2019 champ
q8 = champs.set_index('Year')['Winner'][2019]  # 2019 champion!


##  Questions 9-11: These require the creation of several graphs. In addition to 
##  the code in your Python file, you will also upload a PDF document (not Word!)
##  containing your graphs (be sure they are labeled clearly).  Include the
##  required code in this file and put your graphs in a PDF document for separate
##  submission.  All graphs should have an appropriate title and labels for
##  the axes.  For these questions the only output required are the graphs.
##  When your PDF is ready submit it under 'Assignment 12 Graphs' in Gradescope.

import matplotlib.pyplot as plt

## 9.  For each year of the tournament, determine the average margin of
##     victory for each round.  Then make a histogram of these averages,
##     using 16 bins and a range of [0,32].

# group by year and round, subset MOV, calculate means
avg_mov = df.groupby(['Year', 'Round'])['MOV'].mean()
# create histogram with 16 bins and range [0,32]
plt.hist(avg_mov, bins=16, range=[0,32])
# add X label
plt.xlabel('Margin of Victory')
# add Y label
plt.ylabel('Frequency')
# add title
plt.title('Histogram of Margin of Victory')
# show plot
plt.show()

## 10. Produce side-by-side box-and-whisker plots, one using the Round 1
##     margin of victory for games where the higher seed wins, and one
##     using the Round 1 margin of victory for games where the lower
##     seed wins.  (Remember that higher seed = lower seed number.)
##     Orient the boxes vertically with the higher seed win data on the 
##     left.

# subset first round games where higher seed won, MOV column
higher = df.loc[df['Round'] == 1 & df['Higher_Won'],'MOV']
# calculate Boolean Lower_Won column (necessary to ignore games with same seeds)
df['Lower_Won'] = df['Winning_Seed'] > df['Losing_Seed']
# subset first round games where lower seed won, MOV column
lower = df.loc[df['Round'] == 1 & df['Lower_Won'],'MOV']
# create boxplot
plt.boxplot([higher, lower])
# relabel x ticks
plt.xticks([1, 2], ['Higher', 'Lower'])
# add X label
plt.xlabel('Which Seed Won')
# add Y label
plt.ylabel('Margin of Victory')
# add title
plt.title('Margin of Victory when Higher-vs-Lower Seed Won')
# show plot
plt.show()

## 11. Produce a bar chart for the number of Round 2 victories by seed.
##     The bars should proceed left to right by seed number 1, 2, 3, ...

# subset round 2 winning seeds, value counts
n_R2_wins = df.loc[df['Round'] == 2,'Winning_Seed'].value_counts()
# create bar plot using index and values
plt.bar(n_R2_wins.index, n_R2_wins)
# relabel x ticks to get rid of 0
plt.xticks(list(range(17)), [''] + list(range(1,17)))
# add X label
plt.xlabel('Seed')
# add Y label
plt.ylabel('Number of Round 2 Wins')
# add title
plt.title('Number of Round 2 Wins by Seed')
# show plot
plt.show()
