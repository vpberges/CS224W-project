from snap import *
import collections
import random
import numpy as np
import utils

Graph = TNEANet.New()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)

Graph, EIds = utils.get_graph('training', Graph, EIds)



# PRankH = TIntFltH()
# GetPageRank(Graph, PRankH)
# print 'Snappy Pagerank'
# for item in PRankH:
#     print item, PRankH[item]

def GetWeigth(EId):
	return 1

def GetEdgesIds(NId):
	result = []
	for list_of_EIds in  [EIds[(NId,x)] for x in Graph.GetNI(NId).GetOutEdges()]:
		result += list_of_EIds
	return result
	#raise ('Need to implement GetEdgesIds()')
	#return d[NId]
#How did you count multiple edges connecting between two nodes?

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


