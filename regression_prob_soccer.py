import pandas as pd
import numpy as np
from math import *
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import pylab
from scipy.optimize import curve_fit
from scipy.stats import norm

def sigmoid(x, x0, k):
     y = 1 / (1 + np.exp(-k*(x-x0))) 
     return y

def gauss(x, mu, sigma):
    return 1/(sigma*sqrt(2*pi))*np.exp(-(x-mu)**2/(2.*sigma**2))

def quadratic(x,a,b,c):
	return a*x**2+b*x+c

pagerank = dict()
rating_file = open('ranking/soccer/PR/PR_weighted_age_prob.csv')
for line in rating_file:
	Player, Rating = line.strip().split(',')
	Player, Rating = int(Player), log10(float(Rating))
	pagerank[Player] = round(Rating,1)

df = pd.read_csv("data/train_soccer_prob.csv")
def score(s):
	return round(pagerank[s['WhitePlayer']] - pagerank[s['BlackPlayer']],1)

df['diff_rank'] = df.iloc[:, 1:].apply(score, axis=1)
win = df[['WTEID', 'diff_rank']][df['WhiteScore'] == 1.0].groupby('diff_rank', as_index = False).count()
draw = df[['WTEID', 'diff_rank']][df['WhiteScore'] == 0.5].groupby('diff_rank', as_index = False).count()
loss = df[['WTEID', 'diff_rank']][df['WhiteScore'] == 0.0].groupby('diff_rank', as_index = False).count()

result = pd.merge(win, pd.merge(draw, loss, how='outer', on ='diff_rank'), how = 'outer', on ='diff_rank').fillna(0)
result = result.sort('diff_rank')
result.columns = ['diff_rank', 'win', 'draw', 'loss']
result['total'] = result.win + result.draw + result.loss

xdata = np.asarray(result.diff_rank)[1:-1]
ywin = np.asarray(result['win']/result.total)[1:-1]
ydraw = np.asarray(result['draw']/result.total)[1:-1]
yloss = np.asarray(result['loss']/result.total)[1:-1]

if(True):
	pwin, pcov = curve_fit(quadratic, xdata, ywin)
	pdraw, pcov = curve_fit(quadratic, xdata, ydraw)
	ploss, pcov = curve_fit(quadratic, xdata, yloss)
	x = np.linspace(-1, 1, 21)
	pylab.plot(x,quadratic(x, *pwin), label='Win', color = 'red')
	pylab.plot(x,quadratic(x, *ploss), label='Draw', color = 'green')
	pylab.plot(x,quadratic(x, *pdraw), label='Loss', color = 'blue')
	pylab.ylim(0, 1.05)
	pylab.legend(loc='best')
	pylab.plot(xdata, ywin, 'o', color = 'red')
	pylab.plot(xdata, ydraw, 'o', color = 'green')
	pylab.plot(xdata, yloss, 'o', color = 'blue')
	pylab.show()

d = {'diff_rank':xdata, 'win':quadratic(x, *pwin),'draw':quadratic(x, *pdraw),'loss':quadratic(x, *ploss)}
df = pd.DataFrame(data= d)
df.to_csv('data/predict_soccer.csv', index = False)









