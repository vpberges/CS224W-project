from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import itertools

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

def plot_confusion_matrix(cm, classes,
						  normalize=False,
						  title='Confusion matrix',
						  cmap=plt.cm.Blues):
	"""
	This function prints and plots the confusion matrix.
	Normalization can be applied by setting `normalize=True`.
	"""
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	if normalize:
		cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
		print("Normalized confusion matrix")
	else:
		print('Confusion matrix, without normalization')

	thresh = cm.max() / 2.
	for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, cm[i, j],
				 horizontalalignment="center",
				 color="white" if cm[i, j] > thresh else "black")

	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')

def accuracy(test, rating, **kwargs):
	option = kwargs.get("option", 'All')
	predict = dict()
	label = {}
	with open(test, 'rU') as f:
		next(f)
		for line in f:
			TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, Leaderboard = line.strip().split(',')
			TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore = \
				int(TEID), int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
			predict[TEID] = prediction(rating, WhitePlayer, BlackPlayer)
			label[TEID] = WhiteScore

	y_true = []; y_hat = []
	for TEID in label:
		if predict[TEID] == -1 or label[TEID] == -1:
			continue
		else:
			y_true.append(label[TEID])
			y_hat.append(predict[TEID])
	y_true = np.asarray(y_true)
	y_hat = np.asarray(y_hat)
	return y_true, y_hat

rating = dict()
rating_file = open('initial_ratings.csv')
rating_file.readline()
for line in rating_file:
	Player, Rating, KFactor, NumGames = line.strip().split(',')
	Player, Rating, KFactor, NumGames = int(Player), int(Rating), int(KFactor), int(NumGames)
	rating[Player] = Rating

pagerank = dict()
rating_file = open('output.csv')
rating_file.readline()
for line in rating_file:
	Player, Rating = line.strip().split(',')
	Player, Rating = float(Player), float(Rating)
	pagerank[Player] = Rating

baseline = dict()
rating_file = open('baseline_ranking.csv')
rating_file.readline()
for line in rating_file:
	Player, Rating, draw, loss = line.strip().split(',')
	Player, Rating = float(Player), float(Rating)
	baseline[Player] = Rating

####################Score##################### 
y_true, y_hat = accuracy('test.csv', rating)
print 'absolute score', sum(abs(y_true-y_hat))/len(y_true-y_hat) 
cnf_matrix = confusion_matrix(map(str,y_true), map(str,y_hat))
np.set_printoptions(precision=2)
# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=['win', 'draw', 'loss'],
                      title='Confusion matrix Initial Rating')
plt.show()


y_true1, y_hat1 = accuracy('test.csv', pagerank)
print 'absolute score', sum(abs(y_true1-y_hat1))/len(y_true1-y_hat1) 
cnf_matrix1 = confusion_matrix(map(str,y_true1), map(str,y_hat1))
np.set_printoptions(precision=2)
# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix1, classes=['win', 'draw', 'loss'],
                      title='Confusion matrix Pagerank')
plt.show()

y_true2, y_hat2 = accuracy('test.csv', baseline)
print 'absolute score', sum(abs(y_true2-y_hat2))/len(y_true2-y_hat2) 
cnf_matrix2 = confusion_matrix(map(str,y_true2), map(str,y_hat2))
np.set_printoptions(precision=2)
# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix2, classes=['win', 'draw', 'loss'],
                      title='Confusion matrix Pagerank')
plt.show()

















