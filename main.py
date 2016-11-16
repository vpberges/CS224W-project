from test import *
from label import *


############## Predict Output from Rating ###################
if(False):
	output_prediction('initial_ratings.csv', 'initial_ratings.csv')
	output_prediction('pagerank_weighted_age.csv', 'pagerank_weighted_age.csv')

        args = {'tiebreak':lambda x,y: 2*np.sqrt(x*y) / (x + y + 2*np.sqrt(x*y)) > 0.49, 'testfile':'validation.csv'}
	output_prediction('pagerank_weighted_age.csv', 'pagerank_weighted_age_tiebreak.csv', **args)
	output_probability('pagerank_weighted_age_exp.csv', 'pagerank_weighted_age_tiebreak_probs.csv', **args)

	output_prediction('baseline_ranking.csv', 'baseline.csv')



#############################################################

y_true, y_hat, cnf_matrix = accuracy('test.csv', 'initial_ratings.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'pagerank_weighted_age.csv')
y_true, y_hat, cnf_matrix = accuracy('validation.csv', 'pagerank_weighted_age_tiebreak.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'baseline.csv')

y_true, y_hat, cnf_matrix = accuracy('test.csv', 'LogisticRegressionPredict.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'RandomForestPredict.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'LogisticRegressionPredictNoPRank.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'RandomForestPredictNoPRank.csv')