from snap import *
import collections
import random
import numpy as np
import pandas as pd
import utils
import copy


Graph = TNEANet.New()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)

#Graph, EIds = utils.get_graph('training.csv', Graph, EIds)
Graph, EIds = utils.get_graph('../original_files/primary_training_part1', Graph, EIds)
Graph, EIds = utils.get_graph('../original_files/primary_training_part2', Graph, EIds)
#Graph, EIds = utils.get_graph('very_tiny', Graph, EIds)

def GetEdgesIds(NId):
	result = []
	for list_of_EIds in  [EIds[(NId,x)] for x in Graph.GetNI(NId).GetOutEdges()]:
		result += list_of_EIds
	return result



def GetLinksOrder(A, B, order = 0, visited = []):
	#print A,B,order,visited
	# visited+=[A,B]
	if order==0 :
		n_victory = 0
		n_draw = 0
		n_lost = 0
		for edge in EIds[(A, B)]:
			if Graph.GetIntAttrDatE(edge, 'Weight') == 1 :
				n_lost+=1
			elif Graph.GetIntAttrDatE(edge, 'Weight') == 0 :
				n_draw+=1
		for edge in EIds[(B, A)]:
			if Graph.GetIntAttrDatE(edge, 'Weight') == 1 :
				n_victory+=1
		return {'V':n_victory, 'D':n_draw, 'L':n_lost}, visited
		# return {'V':[str(B)], 'D':[str(B)], 'L':[str(B)]}, visited
	dict_result = {}
	list_intermediates = set([ N for N in Graph.GetNI(A).GetInEdges()]) | set([ N for N in Graph.GetNI(A).GetOutEdges()])
	for N_inter in list_intermediates:
		if N_inter in visited:
			#print N_inter, visited
			continue
			#1+1
		# print 'order : ', order
		old_visited = copy.deepcopy(visited)
		inter_dict, visited = GetLinksOrder(N_inter, B, order - 1, visited +[N_inter])
		visited = old_visited
		# print inter_dict, N_inter, B , order - 1
		n_victory = 0
		n_draw = 0
		n_lost = 0
		for edge in EIds[(A, N_inter)]:
			if Graph.GetIntAttrDatE(edge, 'Weight') == 1 :
				n_lost+=1
			elif Graph.GetIntAttrDatE(edge, 'Weight') == 0 :
				n_draw+=1
		for edge in EIds[(N_inter, A)]:
			if Graph.GetIntAttrDatE(edge, 'Weight') == 1 :
				n_victory+=1
		for key in inter_dict.keys():

			dict_result['V'+key] = dict_result.get('V'+key, 0) + inter_dict.get(key, 0) * n_victory
			dict_result['D'+key] = dict_result.get('D'+key, 0) + inter_dict.get(key, 0) * n_draw    
			dict_result['L'+key] = dict_result.get('L'+key, 0) + inter_dict.get(key, 0) * n_lost

	return dict_result, visited







f = open('training.csv')

table = pd.DataFrame(columns = ['WhitePlayer', 'BlackPlayer', 'TrueWhiteScore', 'V', 'D', 'L'])

PRankH = TIntFltH()
GetPageRank(Graph, PRankH)

max_intermediate = 2


print 'start...'
i=0
for line in f:
	if 'PTID' in line:
		continue
	PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, WhitePlayerPrev, BlackPlayerPrev = line.split(',')
	MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
	tmp_dict = {'WhitePlayer':WhitePlayer, 'BlackPlayer':BlackPlayer, 'TrueWhiteScore':WhiteScore}


	if Graph.IsNode(WhitePlayer) and Graph.IsNode(BlackPlayer):
		for deg in range(max_intermediate+1):
			tmp_dict.update(GetLinksOrder(WhitePlayer, BlackPlayer, order = deg, visited = [WhitePlayer,BlackPlayer])[0])

	#Can add other predictors including a pageRank
	if Graph.IsNode(WhitePlayer):
		list_intermediates = set([ N for N in Graph.GetNI(WhitePlayer).GetInEdges()]) | set([ N for N in Graph.GetNI(WhitePlayer).GetOutEdges()])
		n_victory = 0
		n_draw = 0
		n_lost = 0
		for N_inter in list_intermediates:
			for edge in EIds[(WhitePlayer, N_inter)]:
				if Graph.GetIntAttrDatE(edge, 'Weight') == 1 :
					n_lost+=1
				elif Graph.GetIntAttrDatE(edge, 'Weight') == 0 :
					n_draw+=1
			for edge in EIds[(N_inter, WhitePlayer)]:
				if Graph.GetIntAttrDatE(edge, 'Weight') == 1 :
					n_victory+=1
		tmp_dict['White_V'] = n_victory
		tmp_dict['White_D'] = n_draw
		tmp_dict['White_L'] = n_lost
		tmp_dict['White_PRank'] = PRankH[WhitePlayer]
	if Graph.IsNode(BlackPlayer):
		list_intermediates = set([ N for N in Graph.GetNI(BlackPlayer).GetInEdges()]) | set([ N for N in Graph.GetNI(BlackPlayer).GetOutEdges()])
		n_victory = 0
		n_draw = 0
		n_lost = 0
		for N_inter in list_intermediates:
			for edge in EIds[(BlackPlayer, N_inter)]:
				if Graph.GetIntAttrDatE(edge, 'Weight') == 1 :
					n_lost+=1
				elif Graph.GetIntAttrDatE(edge, 'Weight') == 0 :
					n_draw+=1
			for edge in EIds[(N_inter, BlackPlayer)]:
				if Graph.GetIntAttrDatE(edge, 'Weight') == 1 :
					n_victory+=1
		tmp_dict['Black_V'] = n_victory
		tmp_dict['Black_D'] = n_draw
		tmp_dict['Black_L'] = n_lost
		tmp_dict['Black_PRank'] = PRankH[BlackPlayer]





	i+=1

	# if i>20:
	# 	break
	table = table.append(pd.DataFrame(tmp_dict, index = [i]))
	if i % 500 == 0 :
		table.to_csv('localDataFrame.csv')
		print i

table = table.append(pd.DataFrame(tmp_dict, index = [i]))
table.to_csv('localDataFrame.csv')

