import collections
import random
import numpy as np
import pandas as pd
import utils
import copy

from snap import *

from sklearn import linear_model, datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
np.random.seed(1)

#addOn = ''
# addOn = 'NoLoops'
# addOn = '_basketball_'
addOn = '_soccer_'


test_file = 'data/test.csv'
if  'soccer' in addOn:
	test_file = 'data/test_soccer.csv'
if 'basketball' in addOn:
	test_file = 'data/test_basketball.csv'

train = pd.read_csv('data/val'+addOn+'Features.csv').fillna(0)#.drop('Unnamed: 0',1)
#train = train.drop('Black_PRank', 1).drop('White_PRank', 1)
test = pd.read_csv('data/test'+addOn+'Features.csv').fillna(0)#.drop('Unnamed: 0',1)
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
# This is the Fine Tuning part
'''
result = open('BoostingTuning.csv','w')
result.write('Learning_Rate, Number_Trees, Max_Depth, Subsample \n')
for B in [20, 50, 100, 500]:
	for md in [1 , 2, 3]:
		for lr in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5]:
			for subs in [0.5, 0.6,0.7,0.8,0.9,1.0]:
				mod = GradientBoostingClassifier(learning_rate=lr, n_estimators=B, max_depth=md, subsample=subs)

				# mod.fit(train[predictors].as_matrix(), [str(x) for x in list(train.TrueWhiteScore.values)])

				# y_pred = mod.predict(test[predictors].as_matrix())

				# mod = RandomForestClassifier(100)
				np.random.seed(1)
				msk = sorted(np.random.rand(len(train)) < 0.8, reverse = True)
				# msk = [1] * int(len(train)*0.7)
				# msk = msk + [0] * (len(train - len(msk)))
				cv_train = train[: int(len(train) * 0.8)]
				cv_test = train[int(len(train) * 0.8) + 1 :]

				# print '1'

				mod.fit(cv_train[predictors].as_matrix(), [str(x) for x in list(cv_train.TrueWhiteScore.values)])
				y_pred = mod.predict(cv_test[predictors].as_matrix())
				print 'learning_rate : ' ,lr,'\t n_tree : '  , B, '\t max_depth : ' , md,'\tSubsample: ',subs , '\t RMSE : ', sum(abs(float(y_pred[i]) - float(cv_test.TrueWhiteScore.values[i])) for i in range(len(y_pred)))/len(y_pred)
				result.write(str(lr)+','+str(B)+','+str(md)+','+str(subs)+','+str(sum(abs(float(y_pred[i]) - float(cv_test.TrueWhiteScore.values[i])) for i in range(len(y_pred)))/len(y_pred))+'\n')
result.close()'''


mod = GradientBoostingClassifier(learning_rate=0.1, n_estimators=500, max_depth=3, subsample=0.6)

mod.fit(train[predictors].as_matrix(), [str(x) for x in list(train.TrueWhiteScore.values)])

y_pred = mod.predict(test[predictors].as_matrix())

importances = mod.feature_importances_
indices = np.argsort(importances)[::-1]
for f in range(train[predictors].shape[1]):
    print f,' : ', predictors[f],' --> ', importances[indices[f]]




points = 0
total = 0
error = 0
f = open('prediction/Boosting'+addOn+'Predict.csv', 'w')

fff = open(test_file, 'Ur')
print fff.readline()
for pred, true in zip(y_pred ,[str(x) for x in list(test.TrueWhiteScore.values)] ):
	if true == -1: continue
	error+= abs(float(pred) - float(true))
	total += 1
	if pred == true:
		points+=1
	f.write(str(fff.readline().split(',')[0])+','+ str(pred) + '\n')
print 'RBoostingClassifier'
print error*1.0 / total
f.close()
fff.close()




