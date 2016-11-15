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

pagerank = dict()
rating_file = open('ranking/pagerank.csv')
for line in rating_file:
	Player, Rating = line.strip().split(',')
	Player, Rating = int(Player), log10(float(Rating))
	pagerank[Player] = round(Rating,1)

df = pd.read_csv("data/training.csv")
def score(s):
	return round(pagerank[s['WhitePlayer']] - pagerank[s['BlackPlayer']],1)

df['diff_rank'] = df.iloc[:, 1:].apply(score, axis=1)
win = df[['PTID', 'diff_rank']][df['WhiteScore'] == 1.0].groupby('diff_rank', as_index = False).count()
draw = df[['PTID', 'diff_rank']][df['WhiteScore'] == 0.5].groupby('diff_rank', as_index = False).count()
loss = df[['PTID', 'diff_rank']][df['WhiteScore'] == 0.0].groupby('diff_rank', as_index = False).count()

result = pd.merge(win, pd.merge(draw, loss, how='outer', on ='diff_rank'), how = 'outer', on ='diff_rank').fillna(0)
result = result.sort('diff_rank')
result.columns = ['diff_rank', 'win', 'draw', 'loss']
result['total'] = result.win + result.draw + result.loss

xdata = np.asarray(result.diff_rank)
ywin = np.asarray(result['win']/result.total)
ydraw = np.asarray(result['draw']/result.total)
yloss = np.asarray(result['loss']/result.total)

if(True):
	pwin, pcov = curve_fit(sigmoid, xdata, ywin)
	pdraw, pcov = curve_fit(gauss, xdata, ydraw)
	ploss, pcov = curve_fit(sigmoid, xdata, yloss)
	x = np.linspace(-2.0, 2.0, 40)
	#pylab.plot(xdata, ydata, 'o', label='data')
	pylab.plot(x,sigmoid(x, *pwin), label='fit', color = 'red')
	pylab.plot(x,sigmoid(x, *ploss), label='fit', color = 'green')
	pylab.plot(x,gauss(x, *pdraw), label='fit', color = 'blue')
	pylab.ylim(0, 1.05)
	pylab.legend(loc='best')
	pylab.show()





