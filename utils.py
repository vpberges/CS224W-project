from snap import *


# Get edges from the edges

a = 6 


def GetListEdges(Graph,N1,N2):
	result = []
	for e in GetOutEdges(Graph.GetNI(N1)):
		print e
		if (Graph.GetEI(e).GetDstNId() == N2):
			result+= [e]
	return result






