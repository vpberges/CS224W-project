from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import itertools


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
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

def accuracy(test, predicted, **kwargs):
	plot = kwargs.get("plot", False)
	predict = {}; label = {}
	test = 'data/' + test
	with open(test, 'rU') as f:
		next(f)
		for line in f:
			TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, Leaderboard = line.strip().split(',')
			TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore = \
					int(TEID), int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
			label[TEID] = WhiteScore

	predicted = 'prediction/' + predicted 
	with open(predicted, 'rU') as f:
		for line in f:
			TEID, WhiteScore = line.strip().split(',')
			TEID, WhiteScore = int(TEID), float(WhiteScore)
			predict[TEID] = WhiteScore

	y_true = []; y_hat = []
	for TEID in label:
		if predict[TEID] == -1 or label[TEID] == -1:
			continue
		else:
			y_true.append(label[TEID])
			y_hat.append(predict[TEID])
	y_true = np.asarray(y_true)
	y_hat = np.asarray(y_hat)
	cnf_matrix = confusion_matrix(map(str,y_true), map(str,y_hat))
	print '############# Method : ', predicted[11:-4], ' ################' 
	print 'Mean Absolute Difference Error: ', sum(abs(y_true-y_hat))/len(y_true-y_hat) 
	print 'Exact Accyracy: ', sum(abs(y_true-y_hat) == 0)*1.0/len(y_true-y_hat) 
	print 'Balanced Accuracy: ', np.trace(cnf_matrix*1.0/np.sum(cnf_matrix, axis = 0))/3.0
	if(plot):
		np.set_printoptions(precision=2)
		# Plot non-normalized confusion matrix
		plt.figure()
		plot_confusion_matrix(cnf_matrix, classes=['win', 'draw', 'loss'], title='Confusion matrix ' + predicted[11:-4])
		plt.show()

	return y_true, y_hat, cnf_matrix




















