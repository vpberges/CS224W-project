import pandas as pd
import numpy as np
from math import *
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import pylab
from scipy.optimize import curve_fit

def sigmoid(x, x0, k, a, c):
     y = a / (1 + np.exp(-k*(x-x0))) + c
     return y


pagerank = dict()
rating_file = open('output.csv')
for line in rating_file:
	Player, Rating = line.strip().split(',')
	Player, Rating = int(Player), log10(float(Rating))
	pagerank[Player] = round(Rating,1)

df = pd.read_csv("training.csv")
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


var = 'win'
tmp = result[var]/result.total

xdata = np.asarray(result.diff_rank)
ydata = np.asarray(tmp)
popt, pcov = curve_fit(sigmoid, xdata, ydata)
print popt

x = np.linspace(-2.0, 2.0, 40)
y = sigmoid(x, *popt)

pylab.plot(xdata, ydata, 'o', label='data')
pylab.plot(x,y, label='fit')
pylab.ylim(0, 1.05)
pylab.legend(loc='best')
pylab.show()




