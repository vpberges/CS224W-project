from snap import *
import collections
import random
import numpy as np
import pandas as pd
import utils
import copy
import sys


# graphFile = 'training.csv'
# trainFile = 'validation.csv'
# nameFile = 'valFeatures.csv'

graphFile = sys.argv[1]
trainFile = sys.argv[2]
nameFile = sys.argv[3]




Graph = TNEANet.New()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)

#Graph, EIds = utils.get_graph('training.csv', Graph, EIds)
#Graph, EIds = utils.get_graph('../original_files/primary_training_part1', Graph, EIds)
#Graph, EIds = utils.get_graph('../original_files/primary_training_part2', Graph, EIds)


Graph, EIds , stats= utils.get_graph(graphFile, Graph, EIds, True)

"""If you want the graph to be different : """
Graph, EIds  =  utils.noLoops(Graph, EIds)



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
		return {'V':n_victory, 'D':n_draw, 'L':n_lost}
		# return {'V':[str(B)], 'D':[str(B)], 'L':[str(B)]}, visited
	dict_result = {}
	list_intermediates = sorted([ N for N in Graph.GetNI(A).GetInEdges()] + [ N for N in Graph.GetNI(A).GetOutEdges()])
	last_element_list = None
	for N_inter in list_intermediates:
		if N_inter == last_element_list :
			continue
		last_element_list = N_inter
		if N_inter in visited:
			#print N_inter, visited
			continue
			#1+1
		# print 'order : ', order
		inter_dict = GetLinksOrder(N_inter, B, order - 1, visited +[N_inter])
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

	return dict_result








f = open(trainFile, 'rU')
#f = open('very_tiny.csv')
output = open(nameFile,'w')
# output.write('DVL,DL,White_D,VDV,DVD,DD,DDL,White_L,Black_L,LLV,VDD,White_V,DV,DVV,VDL,LD,VLL,LDD,VVV,LL,Black_D,VLD,LDL,LV,DDV,VVL,LDV,LLL,VVD,VLV,LVV,VD,D,DLD,White_PRank,VL,BlackPlayer,L,LVD,WhitePlayer,DLV,VV,V,LVL,DLL,DDD,Black_PRank,TrueWhiteScore,LLD,Black_V\n')

#table = pd.DataFrame(columns = ['WhitePlayer', 'BlackPlayer', 'TrueWhiteScore', 'V', 'D', 'L'])

#RankH = TIntFltH()
#GetPageRank(Graph, PRankH)

PRankH = utils.PageRank(Graph, EIds , stats, utils.sigmoidGetWeight)

max_intermediate = 2


print 'start...'
i=0
for line in f:
	if 'MonthID' in line:
		continue
	if   'test.csv' in trainFile:
		PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, Trash = line.split(',')
	else :
		PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, WhitePlayerPrev, BlackPlayerPrev = line.split(',')
	MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
	tmp_dict = {'DVL': 0, 'DL': 0, 'White_D': 0, 'VDV': 0, 'DVD': 0, 'DD': 0, 'DDL': 0, 'White_L': 0, 'Black_L': 0, 'LLV': 0,\
	 'VDD': 0, 'White_V': 0, 'DV': 0, 'DVV': 0, 'VDL': 0, 'LD': 0, 'VLL': 0, 'LDD': 0, 'VVV': 0, 'LL': 0, 'Black_D': 0, 'VLD': 0, \
	 'LDL': 0, 'LV': 0, 'DDV': 0, 'VVL': 0, 'LDV': 0, 'LLL': 0, 'VVD': 0, 'VLV': 0, 'LVV': 0, 'VD': 0, 'D': 0, 'DLD': 0, \
	 'White_PRank': 0, 'VL': 0, 'BlackPlayer': BlackPlayer, 'L': 0, 'LVD': 0, 'WhitePlayer': WhitePlayer, 'DLV': 0, 'VV': 0, 'V': 0, 'LVL': 0, \
	 'DLL': 0, 'DDD': 0, 'Black_PRank': 0, 'TrueWhiteScore': WhiteScore, 'LLD': 0, 'Black_V': 0}


	if Graph.IsNode(WhitePlayer) and Graph.IsNode(BlackPlayer):
		for deg in range(max_intermediate+1):
			try:
				tmp_dict.update(GetLinksOrder(WhitePlayer, BlackPlayer, order = deg, visited = [WhitePlayer,BlackPlayer]))
			except:
				raise





	#Can add other predictors including a pageRank
	if Graph.IsNode(WhitePlayer):
		n_victory = 0
		n_draw = 0
		n_lost = 0
		list_intermediates = sorted([ N for N in Graph.GetNI(WhitePlayer).GetInEdges()] + [ N for N in Graph.GetNI(WhitePlayer).GetOutEdges()])
		last_element_list = None
		for N_inter in list_intermediates:
			if N_inter == last_element_list :
				continue
			last_element_list = N_inter
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
		n_victory = 0
		n_draw = 0
		n_lost = 0
		list_intermediates = sorted([ N for N in Graph.GetNI(BlackPlayer).GetInEdges()] + [ N for N in Graph.GetNI(BlackPlayer).GetOutEdges()])
		last_element_list = None
		for N_inter in list_intermediates:
			if N_inter == last_element_list :
				continue
			last_element_list = N_inter
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


	if i==0:
		output.write('PTID,'+','.join([str(x) for x in tmp_dict.keys()]) + '\n')
	output.write(str(PTID) +','+ ','.join([str(x) for x in tmp_dict.values()]) + '\n')


	#output.write(','.join(tmp_dict.values()))

	i+=1

	# if i>20:
	# 	break
	#table = table.append(pd.DataFrame(tmp_dict, index = [i]))
	#if i % 500 == 0 :
		#table.to_csv('localDataFrame.csv')
		#print i

#table = table.append(pd.DataFrame(tmp_dict, index = [i]))
#table.to_csv('localDataFrame.csv')

f.close()
output.close()

