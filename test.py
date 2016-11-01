from sklearn.metrics import confusion_matrix
import numpy as np

def prediction(rating, player1, player2):
	if player1 not in rating or player2 not in rating:
		return -1.0
	rating1 = rating[player1]
	rating2 = rating[player2]
	if rating1 > rating2:
		return 1.0
	elif rating1 == rating2:
		return 0.5
	else:
		return 0.0

def accuracy(test_set, test_label, rating, **kwargs):
	option = kwargs.get("option", 'All')
	predict = dict()
	test_file = open(test_set) #test_set
	test_file.readline()
	for line in test_file:
		TEID, MonthID, WhitePlayer, BlackPlayer = line.strip().split(',')
		TEID, MonthID, WhitePlayer, BlackPlayer = int(TEID), int(MonthID), int(WhitePlayer), int(BlackPlayer)
		predict[TEID] = prediction(rating, WhitePlayer, BlackPlayer)

	label = {'Real':{}, 'Spurious':{}, 'All': {}}
	label_file = open(test_label)
	label_file.readline()
	for line in label_file:
		TEID, WhiteScore, Leaderboard = line.strip().split(',')
		TEID, WhiteScore = int(TEID), float(WhiteScore)
		if Leaderboard != 'Spurious':
			Leaderboard = 'Real'
		label[Leaderboard][TEID] = WhiteScore
		label['All'][TEID] = WhiteScore

	y_true = []; y_hat = []
	for TEID in label[option]:
		if predict[TEID] == -1 :
			continue
		else:
			y_true.append(label[option][TEID])
			y_hat.append(predict[TEID])
	y_true = np.asarray(y_true)
	y_hat = np.asarray(y_hat)
	return sum(abs(y_true-y_hat))/len(y_true-y_hat) #confusion_matrix(y_true, y_pred)

rating = dict()
rating_file = open('initial_ratings.csv')
rating_file.readline()
for line in rating_file:
	Player, Rating, KFactor, NumGames = line.strip().split(',')
	Player, Rating, KFactor, NumGames = int(Player), int(Rating), int(KFactor), int(NumGames)
	rating[Player] = Rating

y_true, y_hat = accuracy('test.csv', 'test_solution.csv', rating)

