import pandas as pd 
import numpy as np
import glob

df = pd.DataFrame()
for file in glob.glob("data/soccer/*.csv"):
	tmp = pd.read_csv(file)
	df = pd.concat([df,tmp])

df = df[['Referee','Date', 'HomeTeam', 'AwayTeam', 'FTR', 'Div','BbMxH', 'BbMxD', 'BbMxA']]
df = df.dropna(thresh=3)
df.loc[:,'Referee'] = range(1, len(df) + 1)
df.loc[:,'BbMxH'] = 1/df.loc[:,'BbMxH']
df.loc[:,'BbMxD'] = 1/df.loc[:,'BbMxD']
df.loc[:,'BbMxA'] = 1/df.loc[:,'BbMxA']
df.loc[:,'Date'] = pd.to_datetime(df['Date']).dt.year.astype(int)*100+pd.to_datetime(df['Date']).dt.month.astype(int)
teams = set(df.HomeTeam).union(set(df.AwayTeam))
team_id = dict()
count = 0
for team in teams:
	if team not in team_id:
		team_id[team] = count
		count += 1

df = df.replace({"HomeTeam": team_id})
df = df.replace({"AwayTeam": team_id})

result = {'H':1,'A':0,'D':0.5}
df = df.replace({"FTR": result})

data = df[['Referee','Date', 'HomeTeam', 'AwayTeam', 'FTR', 'Div']]
data.columns = ['WTEID','MonthID','WhitePlayer','BlackPlayer','WhiteScore','Leaderboard']

train = data[np.logical_and(data.MonthID > 201406,data.MonthID < 201501)]
valid = data[np.logical_and(data.MonthID >= 201501,data.MonthID <= 201503)]
test = data[np.logical_and(data.MonthID > 201503,data.MonthID < 201506)]

train.to_csv('data/train_soccer.csv', index = False)
valid.to_csv('data/valid_soccer.csv', index = False)
test.to_csv('data/test_soccer.csv', index = False)


odd = df[['Referee', 'BbMxH', 'BbMxD', 'BbMxA']]
odd.columns = ['WTEID','Win','Draw','Loss']
odd.to_csv('data/odd_soccer.csv', index = False)





