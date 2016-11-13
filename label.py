from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import itertools

def prediction(rating, player1, player2, tiebreak_func=(lambda x,y: x==y)):
	if player1 not in rating or player2 not in rating:
		return -1.0
	rating1 = rating[player1]
	rating2 = rating[player2]
	if tiebreak_func(rating1, rating2):
		return 0.5
	elif rating1 > rating2:
		return 1.0
	else:
		return 0.0


def rating_to_dict(filename):
	rating = dict()
	rating_file = open('ranking/' + filename)
	if filename == 'initial_ratings.csv':
		rating_file.readline()
		for line in rating_file:
			Player, Rating, KFactor, NumGames = line.strip().split(',')
			Player, Rating, KFactor, NumGames = int(Player), int(Rating), int(KFactor), int(NumGames)
			rating[Player] = Rating
	elif filename == 'baseline_ranking.csv':
		for line in rating_file:
			Player, Rating, Draw, Loss = line.strip().split(',')
			Player, Rating = float(Player), float(Rating)
			rating[Player] = Rating
	else:
		#elif filename in ['pagerank_weighted_age.csv','pagerank.csv']:
		for line in rating_file:
			Player, Rating = line.strip().split(',')
			Player, Rating = float(Player), float(Rating)
			rating[Player] = Rating
	return rating

def output_prediction(rating, filename, **kwargs):
	rating = rating_to_dict(rating)
	tiebreak = kwargs.get("tiebreak", None)
	predict = {}
	with open('data/test.csv', 'rU') as f:
		next(f)
		for line in f:
			TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, Leaderboard = line.strip().split(',')
			TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore = \
				int(TEID), int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
			if not tiebreak:
				predict[TEID] = prediction(rating, WhitePlayer, BlackPlayer)
			else:
				predict[TEID] = prediction(rating, WhitePlayer, BlackPlayer,tiebreak)
	
	f = open('prediction/'+filename,'w')
	for TEID in predict:
		f.write(str(TEID)+ ','+str(predict[TEID])+'\n')
	f.close()
	return











