from snap import *
import collections
import random
import numpy as np
import utils

Graph = TNEANet.New()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')
EIds = collections.defaultdict(list)

Graph, EIds = utils.get_graph('../original_files/primary_training_part1', Graph, EIds)
print Graph.GetNodes(), Graph.GetEdges()
Graph, EIds = utils.get_graph('../original_files/primary_training_part2', Graph, EIds)
print Graph.GetNodes(), Graph.GetEdges()

