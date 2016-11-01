from snap import *
import collections
import random
import numpy as np
import matplotlib.pyplot as plt

Graph = TNEANet.New()

f = open('primary_training_part1.csv')
f.readline()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)

i=0
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

	# i+=1
	# if i>100:
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
	result = []
	for list_of_EIds in  [EIds[(NId,x)] for x in Graph.GetNI(NId).GetOutEdges()]:
		result += list_of_EIds
	return result
	#raise ('Need to implement GetEdgesIds()')
	#return d[NId]


print 'Iterative Pagerank'
C = 0.85
Eps=1e-4
MaxIter=20
PRankH = TIntFltH()
new_PRankH = TIntFltH()
for N in Graph.Nodes():
	n = N.GetId()
	PRankH[n] = 1.0/Graph.GetNodes()
	new_PRankH[n] = 0

for iteration in range(MaxIter):
	print iteration
	for N in Graph.Nodes():
		n = N.GetId()
		weights_to_add = {}
		for edgeId in GetEdgesIds(n):
			weights_to_add[Graph.GetEI(edgeId).GetDstNId()] = weights_to_add.get(Graph.GetEI(edgeId).GetDstNId(),0) + GetWeigth(edgeId)
		sum_weights = sum(weights_to_add.values())
		for k in weights_to_add.keys():
			
			new_PRankH[k] += weights_to_add[k] * 1.0 / sum_weights * C * PRankH[n] 
		# for K in Graph.Nodes():
		# 	k = K.GetId()
		# 	new_PRankH[k] += (1-C) * PRankH[n] / Graph.GetNodes()
		# if sum_weights == 0:
		# 	for K in Graph.Nodes():
		# 		k = K.GetId()
		# 		new_PRankH[k] += C * PRankH[n] / Graph.GetNodes()

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

for item in PRankH:
    print item, PRankH[item]



PRankH_old = TIntFltH()
GetPageRank(Graph, PRankH_old)
print 'Comparison'
print max([abs(PRankH[N.GetId()] - PRankH_old[N.GetId()]) for N in Graph.Nodes()])


f = open('output.csv','w')
for N in Graph.Nodes():
	n = N.GetId()
	f.write(str(n)+ ','+str(PRankH[n])+'\n')
f.close()

# print 'Matrix PageRank'

# from scipy.sparse import dok_matrix

# # node_indices = {}
# # i=0
# # for N in Graph.Nodes():
# # 	n = N.GetId()
# # 	node_indices[n] = i

# L = dok_matrix((Graph.GetNodes(),Graph.GetNodes()))
# for edge in Graph.Edges():
# 	if True: 	#Check if edge is edge
# 		#L[node_indices[edge.GetSrcNId()],node_indices[edge.GetDstNId()]] += GetWeigth(edge.GetId())
# 		L[edge.GetSrcNId(),edge.GetDstNId()] += GetWeigth(edge.GetId())


# M=L.transpose().dot(np.diag(1./np.asarray([max(1,x) for x in L.sum(1)])))
# #M=L.transpose().dot(1./np.asarray([max(x,1) for x in np.asarray(L.sum(0))[0]]))
# one = np.ones((Graph.GetNodes(),1))
# r = one/Graph.GetNodes()

# for i in range(1,100+1):
# 	#print C/Graph.GetNodes()*one, (1-C)*np.dot(M,r)
# 	r = (1-C)/Graph.GetNodes()*one + C*M.dot(r)
# 	r += (1-sum(r))/Graph.GetNodes()

# PRankH = TIntFltH()

# for N in Graph.Nodes():
# 	n = N.GetId()
# 	#PRankH[n] = r[node_indices[n]]
# 	PRankH[n] = r[n]

# for item in PRankH:
#     print item, PRankH[item]
