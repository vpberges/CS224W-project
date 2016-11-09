from snap import *
import collections
import numpy as np


def get_graph(fileName, Graph, EIds, giveStats=False):
	f = open(fileName.replace('.csv','')+'.csv')
        minMonth = float('inf')
        maxMonth = float('-inf')

	for line in f:
		if 'PTID' in line:
			continue
		PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, WhitePlayerPrev, BlackPlayerPrev = line.split(',')
		MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
                minMonth = min(minMonth, MonthID)
                maxMonth = max(maxMonth, MonthID)
		if not Graph.IsNode(WhitePlayer):
			Graph.AddNode(WhitePlayer)
		if not Graph.IsNode(BlackPlayer):
			Graph.AddNode(BlackPlayer)
		#By convention, if A beat B, the arrow will be A <-- B
		if WhiteScore == 1:
			eId = Graph.AddEdge(BlackPlayer, WhitePlayer)
	                EIds[(BlackPlayer, WhitePlayer)].append(eId)
			Graph.AddIntAttrDatE(eId, 1, 'Weight')
			Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
		if WhiteScore == 0:
			eId = Graph.AddEdge(WhitePlayer, BlackPlayer)
	                EIds[(WhitePlayer, BlackPlayer)].append(eId)
			Graph.AddIntAttrDatE(eId, 1, 'Weight')
			Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
		if WhiteScore == 0.5:
			eId = Graph.AddEdge(WhitePlayer, BlackPlayer)
	                EIds[(WhitePlayer, BlackPlayer)].append(eId)
			Graph.AddIntAttrDatE(eId, 0, 'Weight')
			Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
			eId = Graph.AddEdge(BlackPlayer, WhitePlayer)
	                EIds[(BlackPlayer, WhitePlayer)].append(eId)
			Graph.AddIntAttrDatE(eId, 0, 'Weight')
			Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
        stats = {'minMonth': minMonth, 'maxMonth': maxMonth}
        if giveStats:
            return Graph, EIds, stats
	return Graph, EIds

def GetOutEdgesIds(Graph, NId, EIds):
	result = []
	for list_of_EIds in [EIds[(NId,x)] for x in Graph.GetNI(NId).GetOutEdges()]:
		result += list_of_EIds
	return result

def GetInEdgesIds(Graph, NId, EIds):
	result = []
	for list_of_EIds in [EIds[(x, NId)] for x in Graph.GetNI(NId).GetInEdges()]:
		result += list_of_EIds
	return result

def GetEdgesIds(Graph, NId, EIds):
	result = []
	for list_of_EIds in [EIds[(NId,x)] for x in Graph.GetNI(NId).GetOutEdges()]:
		result += list_of_EIds
	return result

def PageRank(Graph, EIds, stats, GetWeight):
	C = 0.88
	Eps=5e-5
	MaxIter=20
	PRankH = TIntFltH()
	new_PRankH = TIntFltH()
	for N in Graph.Nodes():
		n = N.GetId()
		PRankH[n] = 1.0/Graph.GetNodes()
		new_PRankH[n] = 0

	for iteration in range(MaxIter):
		for N in Graph.Nodes():
			n = N.GetId()
			weights_to_add = {}
			for edgeId in GetEdgesIds(Graph, n, EIds):
				weights_to_add[Graph.GetEI(edgeId).GetDstNId()] = weights_to_add.get(Graph.GetEI(edgeId).GetDstNId(),0) + GetWeight(Graph, edgeId, stats)
			sum_weights = sum(weights_to_add.values())
			for k in weights_to_add.keys():
				
				new_PRankH[k] += weights_to_add[k] * 1.0 / sum_weights * C * PRankH[n] 

		total_sum = sum([new_PRankH[N.GetId()] for N in Graph.Nodes()])
		for N in Graph.Nodes():
			n = N.GetId()
			new_PRankH[n] += (1-total_sum)/Graph.GetNodes()

		if max([abs(new_PRankH[N.GetId()] - PRankH[N.GetId()]) for N in Graph.Nodes()]) < Eps:
			for N in Graph.Nodes():
				n = N.GetId()
				PRankH[n] = new_PRankH[n]
				new_PRankH[n] = 0
			break
		for N in Graph.Nodes():
			n = N.GetId()
			PRankH[n] = new_PRankH[n]
			new_PRankH[n] = 0
	return PRankH

def advancedGetWeight(Graph, EId, stats):
    monthId = Graph.GetIntAttrDatE(EId, 'MonthID')
    baseWeight = 1 if Graph.GetIntAttrDatE(EId,'Weight') else 0.5
    # Oldest month still is weighted as 1/(1+e^(-2))=0.88 of its original value
    return baseWeight * (1.0 / (1 + np.exp(-1.0 * (monthId-stats['minMonth']+2))))
