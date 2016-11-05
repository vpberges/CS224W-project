from snap import *
import collections





def get_graph(fileName, Graph, EIds ):
	f = open(fileName.replace('.csv','')+'.csv')

	

	for line in f:
		if 'PTID' in line:
			continue
		PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, WhitePlayerPrev, BlackPlayerPrev = line.split(',')
		MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
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

	return Graph, EIds

