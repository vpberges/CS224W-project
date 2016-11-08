from snap import *
import collections


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


