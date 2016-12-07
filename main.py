from test import *
from label import *

np.seterr(invalid='raise')

############## Predict Output from Rating ###################
if(False):
	output_prediction('initial_ratings.csv', 'initial_ratings.csv')
        theta = np.exp(0.6)
        args = {'tiebreak':lambda x,y: 2*np.sqrt(x*y) / (x + y + 2*np.sqrt(x*y)) > 0.4983, 'testfile':'test.csv'}
	output_prediction('pagerank_weighted_age_log.csv', 'log_PR/pagerank_weighted_age_log.csv', **args)
        args = {'tiebreak':lambda x,y: (theta**2 - 1) * x * y / ((x+ theta*y)*(theta*x + y)) > 0.288, 'testfile':'test.csv'}
	output_prediction('pagerank_weighted_age_log.csv', 'log_PR/pagerank_weighted_age_log_theta.csv', **args)
        args = {'tiebreak':lambda x,y: 2*np.sqrt(x*y) / (x + y + 2*np.sqrt(x*y)) > 0.498, 'testfile':'test.csv'}
	output_prediction('pagerank_weighted_age_log_noloop.csv', 'log_PR/pagerank_weighted_age_log_noloop.csv', **args)
        args = {'tiebreak':lambda x,y: (theta**2 - 1) * x * y / ((x+ theta*y)*(theta*x + y)) > 0.2875, 'testfile':'test.csv'}
	output_prediction('pagerank_weighted_age_log_noloop.csv', 'log_PR/pagerank_weighted_age_log_noloop_theta.csv', **args)

        args = {'tiebreak':lambda x,y: 2*np.sqrt(x*y) / (x + y + 2*np.sqrt(x*y)) > 0.494, 'testfile':'test.csv'}
	output_prediction('pagerank_weighted_age.csv', 'PR/pagerank_weighted_age.csv', **args)
        args = {'tiebreak':lambda x,y: (theta**2 - 1) * x * y / ((x+ theta*y)*(theta*x + y)) > 0.28, 'testfile':'test.csv'}
	output_prediction('pagerank_weighted_age.csv', 'PR/pagerank_weighted_age_theta.csv', **args)
        args = {'tiebreak':lambda x,y: 2*np.sqrt(x*y) / (x + y + 2*np.sqrt(x*y)) > 0.494, 'testfile':'test.csv'}
	output_prediction('pagerank_weighted_age_noloop.csv', 'PR/pagerank_weighted_age_noloop.csv', **args)
        args = {'tiebreak':lambda x,y: (theta**2 - 1) * x * y / ((x+ theta*y)*(theta*x + y)) > 0.28, 'testfile':'test.csv'}
	output_prediction('pagerank_weighted_age_noloop.csv', 'PR/pagerank_weighted_age_noloop_theta.csv', **args)

        args = {'testfile': 'test_soccer.csv'}
	output_prediction('soccer/PR/PR_weighted_age_noloop.csv', 'soccer/PR/PR_weighted_age_noloop.csv', **args)
	output_prediction('soccer/log_PR/PR_weighted_age_log_noloop.csv', 'soccer/log_PR/PR_weighted_age_log_noloop.csv', **args)
	output_prediction('soccer/PR/PR_weighted_age.csv', 'soccer/PR/PR_weighted_age.csv', **args)
	output_prediction('soccer/log_PR/PR_weighted_age_log.csv', 'soccer/log_PR/PR_weighted_age_log.csv', **args)

        args = {'testfile': 'test_basketball.csv'}
	output_prediction('basketball/PR/PR_weighted_age_noloop.csv', 'basketball/PR/PR_weighted_age_noloop.csv', **args)
	output_prediction('basketball/log_PR/PR_weighted_age_log_noloop.csv', 'basketball/log_PR/PR_weighted_age_log_noloop.csv', **args)
	output_prediction('basketball/PR/PR_weighted_age.csv', 'basketball/PR/PR_weighted_age.csv', **args)
	output_prediction('basketball/log_PR/PR_weighted_age_log.csv', 'basketball/log_PR/PR_weighted_age_log.csv', **args)


#############################################################
#y_true, y_hat, cnf_matrix = accuracy('test.csv', 'random.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'baseline.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'initial_ratings.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'PR/pagerank_weighted_age_tiebreak.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'PR/pagerank_weighted_age_tiebreak_theta.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'log_PR/pagerank_weighted_age_log.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'log_PR/pagerank_weighted_age_log_theta.csv')

y_true, y_hat, cnf_matrix = accuracy('test.csv', 'beat.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'LogisticRegressionPredict.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'RandomForestPredict.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'LogisticRegressionPredictNoPRank.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'RandomForestPredictNoPRank.csv')

y_true, y_hat, cnf_matrix = accuracy('test.csv', 'LogisticRegressionNoLoopsPredict.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'RandomForestNoLoopsPredict.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'LogisticRegressionNoLoopsPredictNoPRank.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'RandomForestNoLoopsPredictNoPRank.csv')
y_true, y_hat, cnf_matrix = accuracy('test.csv', 'trueSkill_tiebreak.csv')


y_true, y_hat, cnf_matrix = accuracy('test_soccer.csv', 'soccer/log_PR/PR_weighted_age_log.csv')
y_true, y_hat, cnf_matrix = accuracy('test_soccer.csv', 'soccer/log_PR/PR_weighted_age_log_noloop.csv')
y_true, y_hat, cnf_matrix = accuracy('test_soccer.csv', 'soccer/PR/PR_weighted_age.csv')
y_true, y_hat, cnf_matrix = accuracy('test_soccer.csv', 'soccer/PR/PR_weighted_age_noloop.csv')
y_true, y_hat, cnf_matrix = accuracy('test_basketball.csv', 'basketball/log_PR/PR_weighted_age_log.csv')
y_true, y_hat, cnf_matrix = accuracy('test_basketball.csv', 'basketball/PR/PR_weighted_age.csv')
y_true, y_hat, cnf_matrix = accuracy('test_soccer.csv', 'soccer/trueSkill.csv')
y_true, y_hat, cnf_matrix = accuracy('test_basketball.csv', 'basketball/trueSkill.csv')
