from snap import *
import collections
import numpy as np


def get_graph(fileName, Graph, EIds, giveStats=False):
	f = open('data/' + fileName.replace('.csv','').replace('data/','')+'.csv')
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
		print '.',
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

def sigmoidGetWeight(Graph, EId, stats):
    monthId = Graph.GetIntAttrDatE(EId, 'MonthID')
    baseWeight = 1 if Graph.GetIntAttrDatE(EId,'Weight') else 0.5
    # Oldest month still is weighted as 1/(1+e^(-2))=0.88 of its original value
    return baseWeight * (1.0 / (1 + np.exp(-1.0 * (monthId-stats['minMonth']+2))))

def expGetWeight(Graph, EId, stats):
    monthId = Graph.GetIntAttrDatE(EId, 'MonthID')
    baseWeight = 1 if Graph.GetIntAttrDatE(EId,'Weight') else 0.5
	# Oldest month is scaled by e^(-1) = 0.37
    return baseWeight * np.exp((monthId-stats['maxMonth'])/(stats['maxMonth']-stats['minMonth']))

def noLoops(Graph, EIds):
	tmp_flag = False
	for N in Graph.Nodes():
		# print N.GetId() ,' : ',N.GetOutDeg()
		# print [n2 for n2 in N.GetOutEdges()]
		# for n2 in N.GetOutEdges():
		# 	print n2
		for n2 in [x for x in N.GetOutEdges()]:
			for edgeId in EIds[(N.GetId(), n2)]:
				if tmp_flag == True:
					tmp_flag = False
					continue
				else :
					if Graph.GetIntAttrDatE(edgeId,'Weight') == 1 :
						if tmp_flag == True : break
						N2 = Graph.GetNI(n2)
						for n3 in [x for x in N2.GetOutEdges()]:
							if tmp_flag == True : break
							for edgeId2 in EIds[(n2, n3)]:
								if tmp_flag == True : break
								if Graph.GetIntAttrDatE(edgeId2,'Weight') == 1 :
									if tmp_flag == True : break
									for edgeId3 in EIds[(n3, N.GetId())]:
										if tmp_flag == True : break
										if Graph.GetIntAttrDatE(edgeId3,'Weight') == 1 :
											#print '----> ',N.GetId(),n2,n3,'----> ', edgeId, edgeId2, edgeId3
											if tmp_flag == True : break
											#We need to remove the edges:
											#print 'key : ',(N.GetId(), n2)
											EIds[(N.GetId(), n2)].remove(edgeId)
											# if EIds[(N.GetId(), n2)] == [] :
											# 	EIds[(N.GetId(), n2)] ='***'
											# 	#EIds.pop((N.GetId(), n2), None)
											EIds[(n2, n3)].remove(edgeId2)
											# if EIds[(n2, n3)] == [] :
											# 	#EIds.pop((n2, n3), None)
											# 	EIds[(n2, n3)] ='***'
											EIds[(n3, N.GetId())].remove(edgeId3)
											# if EIds[(n3, N.GetId())] == [] :
											# 	EIds[(n3, N.GetId())] ='***'
											# 	#EIds.pop((n3, N.GetId()), None)
											Graph.DelEdge(edgeId)
											Graph.DelEdge(edgeId2)
											Graph.DelEdge(edgeId3)
											tmp_flag = True
	for key in EIds.keys():
		if EIds[key] == []:
			EIds.pop(key, None)
	return Graph, EIds



def noDraws(Graph, EIds):
	for edge in Graph.Edges():
		if Graph.GetIntAttrDatE(edge.GetId(),'Weight') == 0 :
			EIds[(edge.GetSrcNId(), edge.GetDstNId())].remove(edge.GetId())
			Graph.DelEdge(edge.GetId())
	for key in EIds.keys():
		if EIds[key] == []:
			EIds.pop(key, None)
	return Graph, EIds


