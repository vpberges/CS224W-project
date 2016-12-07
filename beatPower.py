from snap import *
import collections
import random
import numpy as np
import pandas as pd
import utils
import copy
import sys

Graph = TNEANet.New()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)

# Graph, EIds , stats= utils.get_graph('training', Graph, EIds, True)
# Graph, EIds , stats= utils.get_graph('../original_files/primary_training_part2', Graph, EIds, True)

# Graph, EIds , stats= utils.get_graph('train_basketball', Graph, EIds, True)

Graph, EIds , stats= utils.get_graph('train_soccer', Graph, EIds, True)

### Graph, EIds , stats= utils.get_graph('../original_files/primary_training_part1', Graph, EIds, True)
Graph, EIds  =  utils.noDraws(Graph, EIds)
Graph, EIds  =  utils.noLoops(Graph, EIds)




def BeatPower(Graph, EIds):
	BPower = TIntFltH()
	for N in Graph.Nodes():
		n = N.GetId()
		beatWin = Graph.GetNI(n).GetInDeg()
		beatLos = Graph.GetNI(n).GetOutDeg()
		BPower[n] = (beatWin - beatLos)* 1.0 / (beatWin + beatLos+1)
	return BPower 

BPower = BeatPower(Graph, EIds)

# f = open('ranking/beatRank_basketball.csv','w')

f = open('ranking/beatRank_soccer.csv','w')

for item in BPower:
	f.write( str(item) + ',' + str(BPower[item]) + '\n')
f.close()
