import collections
import math
import numpy as np
import trueskill
from trueskill import Rating, rate_1vs1, setup
from trueskill.backends import cdf

# Set up
env = trueskill.TrueSkill(draw_probability=0.33)


def predict_outcome(rA, rB):
    deltaMu = rA.mu - rB.mu
    rsss = math.sqrt(rA.sigma**2 + rB.sigma**2)
    win_probability = cdf(deltaMu/rsss)
    if win_probability < 0.32:
        return 0
    elif win_probability > 0.70:
        return 1
    else:
        return 0.5

def output_prediction(ratings, outfile, env, **kwargs):
    tiebreak = kwargs.get("tiebreak", None)
    testfile = 'data/' + kwargs.get("testfile", 'test.csv')
    predict = {}
    missing = 0
    with open(testfile, 'rU') as f:
        next(f)
        for line in f:
            if 'test' in testfile:
                TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, Leaderboard = line.strip().split(',')
            else:
                TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore, WhitePlayerPrev, BlackPlayerPrev = line.split(',')
            TEID, MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(TEID), int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
            if WhitePlayer in ratings:
                rW = ratings[WhitePlayer]
            else:
                rW = env.create_rating()
                missing += 1
            if BlackPlayer in ratings:
                rB = ratings[BlackPlayer]
            else:
                rB = env.create_rating()
                missing += 1
            predict[TEID] = predict_outcome(rW, rB)
    print missing
    f = open('prediction/'+outfile,'w')
    for TEID in predict:
        f.write(str(TEID)+ ','+str(predict[TEID])+'\n')
    f.close()
    return predict

    # Set up
    #mu = 25.0
    #sigma= mu / 3
    #beta = sigma / 2
    #tau = sigma / 100
    #draw_probability = 0.3

    #trueskill.setup(mu, sigma, beta, tau, draw_probability)
def calc_trueskill(fileName, env):
    # Ratings by playerId
    ratings = {}
    try:
        print 'data/' + fileName.replace('.csv','').replace('data/','')+'.csv'
        f = open('data/' + fileName.replace('.csv','').replace('data/','')+'.csv')
    except:
        f = open(fileName.replace('.csv','').replace('data/','')+'.csv')
    for line in f:
        if 'PTID' in line or 'WTEID' in line:
            continue
        PTID, MonthID, WhitePlayer, BlackPlayer, WhiteScore = line.split(',')[:5]
        MonthID, WhitePlayer, BlackPlayer, WhiteScore = int(MonthID), int(WhitePlayer), int(BlackPlayer), float(WhiteScore)
        missing =0
        if WhitePlayer not in ratings:
            ratings[WhitePlayer] = env.create_rating()
            missing += 1
        if BlackPlayer not in ratings:
            ratings[BlackPlayer] = env.create_rating()
            missing += 1
        if WhiteScore == 1:
            ratings[WhitePlayer], ratings[BlackPlayer] = rate_1vs1(ratings[WhitePlayer], ratings[BlackPlayer])
        if WhiteScore == 0:
            ratings[BlackPlayer], ratings[WhitePlayer] = rate_1vs1(ratings[BlackPlayer], ratings[WhitePlayer])
        if WhiteScore == 0.5:
            ratings[WhitePlayer], ratings[BlackPlayer] = rate_1vs1(ratings[WhitePlayer], ratings[BlackPlayer], drawn=True)
    f = open('ranking/basketball/trueskill_ratings.csv','w')
    for Id, r in ratings.iteritems():
        f.write(str(Id)+ ','+str(r.mu)+str(r.sigma)+'\n')
    f.close()
    return ratings

# Output predictions to file
ratings = calc_trueskill('train_basketball',env)
args = {'testfile': 'test_basketball.csv'}
pred = output_prediction(ratings, 'basketball/trueSkill_tiebreak.csv', env, **args) 
