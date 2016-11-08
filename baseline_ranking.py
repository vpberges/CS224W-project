from snap import *
import collections
import random
import numpy as np
import utils

#def baseline_ranking(file):
Graph = TNEANet.New()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)

Graph, EIds = utils.get_graph('training', Graph, EIds)

node_stat = {}
for N in Graph.Nodes():
	nodeID = N.GetId()
	win = 0; loss = 0; draw1 = 0; draw2 = 0
	for edgeId in utils.GetOutEdgesIds(Graph, nodeID, EIds):
		if Graph.GetIntAttrDatE(edgeId, 'Weight') == 1:
			loss += 1
		elif Graph.GetIntAttrDatE(edgeId, 'Weight') == 0:
			draw1 += 1
	for edgeId in utils.GetInEdgesIds(Graph, nodeID, EIds):
		if Graph.GetIntAttrDatE(edgeId, 'Weight') == 1:
			win += 1
		elif Graph.GetIntAttrDatE(edgeId, 'Weight') == 0:
			draw2 += 1
	#print 'draw1', draw1
	#print 'draw2', draw2
	count = win + draw1 + loss; count = float(count)
	node_stat[nodeID] = {'win':win/count, 'draw':draw1/count, 'loss':loss/count}

f = open('baseline_ranking.csv','w')
for N in Graph.Nodes():
	n = N.GetId()
	f.write(str(n)+ ','+str(node_stat[n]['win'])+','+str(node_stat[n]['draw'])+','+str(node_stat[n]['loss'])+'\n')
f.close()


