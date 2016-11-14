import collections
import random
import numpy as np
import pandas as pd
import utils
import copy

from snap import *

from sklearn import linear_model, datasets
from sklearn.ensemble import RandomForestClassifier


train = pd.read_csv('data/valFeatures.csv').fillna(0)#.drop('Unnamed: 0',1)
#train = train.drop('Black_PRank', 1).drop('White_PRank', 1)
test = pd.read_csv('data/testFeatures.csv').fillna(0)#.drop('Unnamed: 0',1)
#test = test.drop('Black_PRank', 1).drop('White_PRank', 1)
# test = test[test.TrueWhiteScore >= 0]

def spe_log(x):
	if x == 0 :
		return -7
	else:
		return np.log(x)

train['Black_PRank'] = train['Black_PRank'].apply(spe_log)
test['Black_PRank'] = test['Black_PRank'].apply(spe_log)
train['White_PRank'] = train['White_PRank'].apply(spe_log)
test['White_PRank'] = test['White_PRank'].apply(spe_log)

train['PRank_ratio'] = train['Black_PRank'] - train['White_PRank']
test['PRank_ratio'] = test['Black_PRank'] - test['White_PRank']

# train['PR_ratio'] = np.log(train['Black_PRank']) - np.log(train['White_PRank'])
# test['PR_ratio'] = np.log(test['Black_PRank']) - np.log(test['White_PRank'])

'''
table = pd.read_csv('data/testFeatures.csv').fillna(0)#.drop('Unnamed: 0',1)
table = table[table.TrueWhiteScore >= 0]
table = table.drop('Black_PRank', 1).drop('White_PRank', 1)
msk = np.random.rand(len(table)) < 0.8
train = table[msk]
test = table[~msk]
'''

predictors = list(train.columns.values)

predictors.remove('WhitePlayer')
predictors.remove('BlackPlayer')
predictors.remove('TrueWhiteScore')
try :
	predictors.remove('PTID')
except:
	pass




logreg = linear_model.LogisticRegression(C=1e5)

logreg.fit(train[predictors].as_matrix(), [str(x) for x in list(train.TrueWhiteScore.values)])

y_pred = logreg.predict(test[predictors].as_matrix())


points = 0
total = 0
error = 0
f = open('prediction/LogisticRegressionPredict.csv', 'w')
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	# for pred, ptid_true in zip(y_pred ,[(ptid, true) for x in zip([str(x) for x in list(test.PTID.values)] ,\
	# 	[str(x) for x in list(test.TrueWhiteScore.values)] )] ):
	error+= abs(float(pred) - float(true))
	total += 1
	f.write(str(total)+','+ str(pred) + '\n')
print 'LogisticRegression'
print error*1.0 / total
f.close()



mod = RandomForestClassifier(100)

mod.fit(train[predictors].as_matrix(), [str(x) for x in list(train.TrueWhiteScore.values)])

y_pred = mod.predict(test[predictors].as_matrix())


points = 0
total = 0
error = 0
f = open('prediction/RandomForestPredict.csv', 'w')
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	if true == -1: continue
	error+= abs(float(pred) - float(true))
	total += 1
	if pred == true:
		points+=1
	f.write(str(total)+','+ str(pred) + '\n')
print 'RandomForestClassifier'
print error*1.0 / total
f.close()


print 'Linear Lasso'
mod = linear_model.Lasso(0.4)

mod.fit(train[predictors].as_matrix(), [float(x) for x in list(train.TrueWhiteScore.values)])

y_pred = mod.predict(test[predictors].as_matrix())

points = 0
total = 0
error = 0
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	if true == -1: continue
	error+= abs(float(pred) - float(true))
	total += 1
	if pred == true:
		points+=1

print error*1.0 / total


print 'Random'
y_pred = [str(x) for x in list(test.TrueWhiteScore.values)]
random.shuffle(y_pred)

points = 0
total = 0
error = 0
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	error+= abs(float(pred) - float(true))
	total += 1
	if pred == true:
		points+=1

print error*1.0 / total




