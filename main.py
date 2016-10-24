from snap import *
import random
import numpy as np
import matplotlib.pyplot as plt

Graph = TNEANet.New()

f = open('primary_training_part1.csv')
f.readline()
Graph.AddIntAttrE('Weight')
Graph.AddIntAttrE('MonthId')

# i=0
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
		Graph.AddIntAttrDatE(eId, 1, 'Weight')
		Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
	if WhiteScore == 0:
		eId = Graph.AddEdge(WhitePlayer, BlackPlayer)
		Graph.AddIntAttrDatE(eId, 1, 'Weight')
		Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
	if WhiteScore == 0.5:
		eId = Graph.AddEdge(WhitePlayer, BlackPlayer)
		Graph.AddIntAttrDatE(eId, 0, 'Weight')
		Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')
		eId = Graph.AddEdge(BlackPlayer, WhitePlayer)
		Graph.AddIntAttrDatE(eId, 0, 'Weight')
		Graph.AddIntAttrDatE(eId, MonthID, 'MonthID')

	# i+=1
	# if i>1000:
	# 	break

PrintInfo(Graph, "QA Stats", "qa-info.txt", False)


