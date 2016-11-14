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

Graph, EIds , stats= utils.get_graph(graphFile, Graph, EIds, True)


def specialWeight(Graph, EId, stats):
    return 1 if Graph.GetIntAttrDatE(EId,'Weight') else 0.5

PRank_Special = utils.PageRank(Graph, EIds, stats, specialWeight)



def noDrawWeight(Graph, EId, stats):
    return 1 if Graph.GetIntAttrDatE(EId,'Weight') else 0

PRank_Special_NoDraws = utils.PageRank(Graph, EIds, stats, noDrawWeight)

Graph, EIds = utils.noLoops(Graph, EIds)

PRank_Special_NoLoops = utils.PageRank(Graph, EIds, stats, specialWeight)
PRank_Special_NoDraws_NoLoops = utils.PageRank(Graph, EIds, stats, noDrawWeight)





def getDistance(A, B, Graph):
	if (Graph.IsNode(A)) and (Graph.IsNode(B)):
		return GetShortPath(Graph, A, B, True)
	else:
		return -1









f = open(trainFile, 'rU')
#f = open('very_tiny.csv')
output = open(nameFile,'w')
# output.write('DVL,DL,White_D,VDV,DVD,DD,DDL,White_L,Black_L,LLV,VDD,White_V,DV,DVV,VDL,LD,VLL,LDD,VVV,LL,Black_D,VLD,LDL,LV,DDV,VVL,LDV,LLL,VVD,VLV,LVV,VD,D,DLD,White_PRank,VL,BlackPlayer,L,LVD,WhitePlayer,DLV,VV,V,LVL,DLL,DDD,Black_PRank,TrueWhiteScore,LLD,Black_V\n')

#table = pd.DataFrame(columns = ['WhitePlayer', 'BlackPlayer', 'TrueWhiteScore', 'V', 'D', 'L'])

#RankH = TIntFltH()
#GetPageRank(Graph, PRankH)

# PRankH = utils.PageRank(Graph, EIds , stats, utils.advancedGetWeight)




print 'start...'
i=0
for line in f:
	if 'MonthID' in line:
		continue
	if trainFile == 'test.csv':
		PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, Trash = line.split(',')
	else :
		PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, WhitePlayerPrev, BlackPlayerPrev = line.split(',')
	MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
	tmp_dict = { 'BlackPlayer': BlackPlayer,  'WhitePlayer': WhitePlayer, 'TrueWhiteScore': WhiteScore,\
	'White_PRank_Special':0, 'Black_PRank_Special':0 ,'Shortest_W_B':0 , 'Shortest_B_W':0,\
	'White_PRank_Special_NoDraws':0, 'White_PRank_Special_NoLoops':0, 'White_PRank_Special_NoDraws_NoLoops':0,
	'Black_PRank_Special_NoDraws':0, 'Black_PRank_Special_NoLoops':0, 'Black_PRank_Special_NoDraws_NoLoops':0}



	if (Graph.IsNode(WhitePlayer)) :
		tmp_dict['White_PRank_Special'] = np.log(PRank_Special[WhitePlayer])
		tmp_dict['White_PRank_Special_NoDraws'] = np.log(PRank_Special_NoDraws[WhitePlayer])
		tmp_dict['White_PRank_Special_NoLoops'] = np.log(PRank_Special_NoLoops[WhitePlayer])
		tmp_dict['White_PRank_Special_NoDraws_NoLoops'] = np.log(PRank_Special_NoDraws_NoLoops[WhitePlayer])
	if (Graph.IsNode(BlackPlayer)):
		tmp_dict['Black_PRank_Special'] = np.log(PRank_Special[BlackPlayer])
		tmp_dict['Black_PRank_Special_NoDraws'] = np.log(PRank_Special_NoDraws[BlackPlayer])
		tmp_dict['Black_PRank_Special_NoLoops'] = np.log(PRank_Special_NoLoops[BlackPlayer])
		tmp_dict['Black_PRank_Special_NoDraws_NoLoops'] = np.log(PRank_Special_NoDraws_NoLoops[BlackPlayer])
	if (Graph.IsNode(WhitePlayer)) and (Graph.IsNode(BlackPlayer)):
		#Need the graph to be the original one...
		tmp_dict['Shortest_W_B'] = getDistance(WhitePlayer, BlackPlayer, Graph)
		tmp_dict['Shortest_B_W'] = getDistance(BlackPlayer, WhitePlayer, Graph)



	if i==0:
		output.write('PTID,'+','.join([str(x) for x in tmp_dict.keys()]) + '\n')
	output.write(str(PTID) +','+ ','.join([str(tmp_dict[x]) for x in tmp_dict.keys()]) + '\n')


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

