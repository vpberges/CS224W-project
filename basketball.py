import pandas as pd 
import numpy as np

df = pd.read_csv('data/basketball.csv')
data = df.query('Season == 2015')
data = data[data.Wloc != 'N']
#convert to day
data.loc[:,'Daynum'] = data.loc[:,'Daynum'] + 365*(data.loc[:,'Season']-1985)
# homw away
data["Wteam"], data["Lteam"] = np.where(data['Wloc']=='H', [data["Wteam"], data["Lteam"]], [data["Lteam"], data["Wteam"]])
data.loc[:,'Season'] = range(1, len(data) + 1)
data.loc[:,'WhiteScore'] = (data.loc[:,'Wloc'] == 'H').astype(int)
data = data[['Season', 'Daynum', 'Wteam', 'Lteam', 'WhiteScore','Numot']]
data.columns = ['WTEID','MonthID','WhitePlayer','BlackPlayer','WhiteScore','Leaderboard']

N = len(data)
start1 = int(N*0.6)
start2 = int(N*0.8)
train = data[0:start1]
valid = data[start1:start2]
test = data[start2:]

train.to_csv('data/train_basketball.csv', index = False)
valid.to_csv('data/valid_basketball.csv', index = False)
test.to_csv('data/test_basketball.csv', index = False)





