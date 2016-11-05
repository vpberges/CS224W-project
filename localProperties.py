from snap import *
import collections
import random
import numpy as np
import pandas as pd
import utils


Graph = TNEANet.New()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)

#Graph, EIds = utils.get_graph('training.csv', Graph, EIds)
#Graph, EIds = utils.get_graph('../original_files/primary_training_part1', Graph, EIds)
Graph, EIds = utils.get_graph('../original_files/primary_training_part2', Graph, EIds)

f = open('training.csv')

table = pd.DataFrame(columns = ['WhitePlayer', 'BlackPlayer', 'TrueWhiteScore', 'V', 'D', 'L'])

i=0
for line in f:
	if 'PTID' in line:
		continue
	PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, WhitePlayerPrev, BlackPlayerPrev = line.split(',')
	MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
	tmp_dict = {'WhitePlayer':WhitePlayer, 'BlackPlayer':BlackPlayer, 'TrueWhiteScore':WhiteScore}

	#Number of V (victory):
	for edge in EIds[(WhitePlayer,BlackPlayer)]:
		print Graph.GetIntAttrDatE(edge, 'Weight')





	table = table.append(pd.DataFrame(tmp_dict, index = [i]))
	table.to_csv('localDataFrame.csv')
	i+=1
	if i>20:
		break
