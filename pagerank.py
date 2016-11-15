from snap import *
import collections
import random
import numpy as np
import utils

Graph = TNEANet.New()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)
#
Graph, EIds, stats = utils.get_graph('training', Graph, EIds, True)

PRankH = utils.PageRank(Graph, EIds, stats, utils.sigmoidGetWeight)
#PRankH = utils.PageRank(Graph, EIds, stats, utils.expGetWeight)

f = open('ranking/pagerank_weighted_age.csv','w')
for N in Graph.Nodes():
	n = N.GetId()
	f.write(str(n)+ ','+str(PRankH[n])+'\n')
f.close()


