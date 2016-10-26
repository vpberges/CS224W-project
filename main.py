from snap import *
import random
import numpy as np
import matplotlib.pyplot as plt

Graph = TNEANet.New()

f = open('primary_training_part1.csv')
f.readline()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')


# i=0
for line in f:
	PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, WhitePlayerPrev, BlackPlayerPrev = line.split(',')
	MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
	if not Graph.IsNode(WhitePlayer):
		Graph.AddNode(WhitePlayer)
	if not Graph.IsNode(BlackPlayer):
		Graph.AddNode(BlackPlayer)
	#By convention, if A beat B, the arrow will be A <-- B
	if WhiteScore == 1:
		eId = Graph.AddEdge(BlackPlayer, WhitePlayer)
		Graph.AddIntAttrDatE(eId, 1, 'Weight')
		Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
	if WhiteScore == 0:
		eId = Graph.AddEdge(WhitePlayer, BlackPlayer)
		Graph.AddIntAttrDatE(eId, 1, 'Weight')
		Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
	if WhiteScore == 0.5:
		eId = Graph.AddEdge(WhitePlayer, BlackPlayer)
		Graph.AddIntAttrDatE(eId, 0, 'Weight')
		Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
		eId = Graph.AddEdge(BlackPlayer, WhitePlayer)
		Graph.AddIntAttrDatE(eId, 0, 'Weight')
		Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')

	# i+=1
	# if i>1000:
	# 	break

# PrintInfo(Graph, "QA Stats", "qa-info.txt", False)


# Graph = TNEANet.New()
# d = {0:[],1:[],2:[],3:[]}
# Graph.AddNode(0)
# Graph.AddNode(1)
# Graph.AddNode(2)
# Graph.AddNode(3)
# d[1]+= [Graph.AddEdge(1,2)]
# d[1]+= [Graph.AddEdge(1,2)]
# d[1]+= [Graph.AddEdge(1,3)]
# d[2]+= [Graph.AddEdge(2,3)]



PRankH = TIntFltH()
GetPageRank(Graph, PRankH)
print 'Snappy Pagerank'
for item in PRankH:
    print item, PRankH[item]

def GetWeigth(EId):
	return 1

def GetEdgesIds(NId):
	"To implement "
	raise ('Need to implement GetEdgesIds()')
	return d[NId]

print 'Perso Pagerank'
C = 0.85
Eps=1e-4
MaxIter=10
PRankH = TIntFltH()
new_PRankH = TIntFltH()
for n in range(Graph.GetNodes()):
	PRankH[n] = 1.0/Graph.GetNodes()
	new_PRankH[n] = 0

for iteration in range(MaxIter):
	for n in range(Graph.GetNodes()):
		weights_to_add = {}
		for edgeId in GetEdgesIds(n):
			weights_to_add[Graph.GetEI(edgeId).GetDstNId()] = weights_to_add.get(Graph.GetEI(edgeId).GetDstNId(),0) + GetWeigth(edgeId)
		sum_weights = sum(weights_to_add.values())
		for k in weights_to_add.keys():
			new_PRankH[k] += weights_to_add[k]*1.0 / sum_weights * C * PRankH[n] 
		for k in range(Graph.GetNodes()):
			new_PRankH[k] += (1-C) * PRankH[n] / Graph.GetNodes()
		if sum_weights == 0:
			for k in range(Graph.GetNodes()):
				new_PRankH[k] += C * PRankH[n] / Graph.GetNodes()
	if max([abs(new_PRankH[n] - PRankH[n]) for n in range(Graph.GetNodes())]) < Eps:
		for n in range(Graph.GetNodes()):
			PRankH[n] = new_PRankH[n]
			new_PRankH[n] = 0
		break
	for n in range(Graph.GetNodes()):
		PRankH[n] = new_PRankH[n]
		new_PRankH[n] = 0

for item in PRankH:
    print item, PRankH[item]



