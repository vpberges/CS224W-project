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
Graph, EIds, stats = utils.get_graph('train_soccer', Graph, EIds, True)
print Graph.GetNodes(), Graph.GetEdges()
#Graph, EIds = utils.noLoops(Graph, EIds)
PRankH = utils.PageRank(Graph, EIds, stats, utils.sigmoidGetWeight)
#PRankH = utils.PageRank(Graph, EIds, stats, utils.expGetWeight)

f = open('ranking/soccer/PR/PR_weighted_age.csv','w+')
for N in Graph.Nodes():
	n = N.GetId()
	f.write(str(n)+ ','+str(PRankH[n])+'\n')
f.close()

logPRank = {N.GetId(): np.log(PRankH[N.GetId()]) for N in Graph.Nodes()}
minPR = min(logPRank.values()) - 0.001

f = open('ranking/soccer/log_PR/PR_weighted_age_log.csv','w+')
for N in Graph.Nodes():
	n = N.GetId()
	f.write(str(n)+ ','+str(np.log(PRankH[n]) - minPR) +'\n')
f.close()

Graph, EIds = utils.noLoops(Graph, EIds)
PRankH = utils.PageRank(Graph, EIds, stats, utils.sigmoidGetWeight)

f = open('ranking/soccer/PR/PR_weighted_age_noloop.csv','w+')
for N in Graph.Nodes():
	n = N.GetId()
	f.write(str(n)+ ','+str(PRankH[n])+'\n')
f.close()

logPRank = {N.GetId(): np.log(PRankH[N.GetId()]) for N in Graph.Nodes()}
minPR = min(logPRank.values()) - 0.001

f = open('ranking/soccer/log_PR/PR_weighted_age_log_noloop.csv','w+')
for N in Graph.Nodes():
	n = N.GetId()
	f.write(str(n)+ ','+str(np.log(PRankH[n]) - minPR) +'\n')
f.close()

