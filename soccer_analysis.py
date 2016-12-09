import pandas as pd 
import numpy as np
from math import *

pagerank = dict()
rating_file = open('ranking/soccer/PR/PR_weighted_age_prob.csv')
for line in rating_file:
	Player, Rating = line.strip().split(',')
	Player, Rating = int(Player), log10(float(Rating))
	pagerank[Player] = round(Rating,1)

df = pd.read_csv("data/odd_soccer.csv")
#check player in df
def score(s):
	if s['WhitePlayer'] not in pagerank.keys() or s['BlackPlayer'] not in pagerank.keys():
		return 1.5
	return round(pagerank[s['WhitePlayer']] - pagerank[s['BlackPlayer']],1)

df['diff_rank'] = df.iloc[:, 1:].apply(score, axis=1)
df = df[np.logical_and(df.diff_rank < 1.1, df.diff_rank > -1.1)]

predict = pd.read_csv('data/predict_soccer.csv')

def pwin(s):
	return round(predict[predict.diff_rank == float(s['diff_rank'])]['win'].values[0] - s['Win'],3)

def ploss(s):
	return round(predict[predict.diff_rank == float(s['diff_rank'])]['loss'].values[0] - s['Loss'],3)

def pdraw(s):
	return round(predict[predict.diff_rank == float(s['diff_rank'])]['draw'].values[0] - s['Draw'],3)


df['delta_win'] = df.iloc[:, 1:].apply(pwin, axis=1)
df['delta_loss'] = df.iloc[:, 1:].apply(ploss, axis=1)
df['delta_draw'] = df.iloc[:, 1:].apply(pdraw, axis=1)
df.to_csv('data/soccer_result.csv', index = False)