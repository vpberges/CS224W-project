import collections
import random
import numpy as np
import pandas as pd
import utils
import copy


from sklearn import linear_model, datasets
from sklearn.ensemble import RandomForestClassifier


table = pd.read_csv('localPropertiesSecondDataFrame.csv').fillna(0)#.drop('Unnamed: 0',1)
predictors = list(table.columns.values)

predictors.remove('WhitePlayer')
predictors.remove('BlackPlayer')
predictors.remove('TrueWhiteScore')
try :
	predictors.remove('PTID')
except:
	pass

msk = np.random.rand(len(table)) < 0.8
train = table[msk]
test = table[~msk]

logreg = linear_model.LogisticRegression(C=1e5)

logreg.fit(train[predictors].as_matrix(), [str(x) for x in list(train.TrueWhiteScore.values)])

y_pred = logreg.predict(test[predictors].as_matrix())


points = 0
total = 0
error = 0
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	error+= abs(float(pred) - float(true))
	total += 1
	if pred == true:
		points+=1
print 'LogisticRegression'
print points *1.0 / total, error*1.0 / total




mod = RandomForestClassifier(100)

mod.fit(train[predictors].as_matrix(), [str(x) for x in list(train.TrueWhiteScore.values)])

y_pred = mod.predict(test[predictors].as_matrix())


points = 0
total = 0
error = 0
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	error+= abs(float(pred) - float(true))
	total += 1
	if pred == true:
		points+=1

print 'RandomForestClassifier'
print points *1.0 / total, error*1.0 / total


print 'Linear Lasso'
mod = linear_model.Lasso(0.4)

mod.fit(train[predictors].as_matrix(), [float(x) for x in list(train.TrueWhiteScore.values)])

y_pred = mod.predict(test[predictors].as_matrix())

points = 0
total = 0
error = 0
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	error+= abs(float(pred) - float(true))
	total += 1
	if pred == true:
		points+=1

print points *1.0 / total, error*1.0 / total


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

print points *1.0 / total, error*1.0 / total

print total



