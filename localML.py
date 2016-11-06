import collections
import random
import numpy as np
import pandas as pd
import utils
import copy


from sklearn import linear_model, datasets
from sklearn.ensemble import RandomForestClassifier


table = pd.read_csv('localDataFrame.csv').fillna(0).drop('Unnamed: 0',1)
predictors = list(table.columns.values)

predictors.remove('WhitePlayer')
predictors.remove('BlackPlayer')
predictors.remove('TrueWhiteScore')

msk = np.random.rand(len(table)) < 0.8
train = table[msk]
test = table[~msk]

logreg = linear_model.LogisticRegression(C=1e5)

logreg.fit(train[predictors].as_matrix(), [str(x) for x in list(train.TrueWhiteScore.values)])

y_pred = logreg.predict(test[predictors].as_matrix())


points = 0
total = 0
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	total += 1
	if pred == true:
		points+=1

print points *1.0 / total



mod = RandomForestClassifier()

mod.fit(train[predictors].as_matrix(), [str(x) for x in list(train.TrueWhiteScore.values)])

y_pred = mod.predict(test[predictors].as_matrix())


points = 0
total = 0
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	total += 1
	if pred == true:
		points+=1

print points *1.0 / total

print total