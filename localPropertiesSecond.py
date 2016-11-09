from snap import *
import collections
import random
import numpy as np
import pandas as pd
import utils
import copy




graphTable = pd.read_csv('train.csv')[['WhitePlayer','BlackPlayer','WhiteScore']]
#graphTable = pd.read_csv('test.csv')[['WhitePlayer','BlackPlayer','WhiteScore']]

# graphTable = graphTable[0:4000]

# graphTable.columns = ['Player1','Player2','Score']
# victoryTable = graphTable[graphTable.Score == 1.0][['Player1','Player2']]
# lostTable = graphTable[graphTable.Score == 0.0][['Player1','Player2']]
# drawTable = graphTable[graphTable.Score == 0.5][['Player1','Player2']]
# secondVictoryTable = lostTable.copy()
# secondVictoryTable.columns = ['Player2','Player1']
# secondLostTable = victoryTable.copy()
# secondLostTable.columns = ['Player2','Player1']


# lostTable = lostTable.append(secondLostTable)
# victoryTable = victoryTable.append(secondVictoryTable)


# lostTable['Outcome'] = 'L'
# drawTable['Outcome'] = 'D'
# victoryTable['Outcome'] = 'V'

# graphTable = lostTable.append(drawTable.append(victoryTable))

def func(row):
    if row['Score'] == 0:
        return 'L'
    elif row['Score'] ==1:
        return 'V' 
    else:
        return 'D'

def func2(row):
    if row['Outcome'] == 'V':
        return 'L'
    elif row['Outcome'] =='L':
        return 'V' 
    else:
        return 'D'

print '.'
graphTable.columns = ['Player1','Player2','Score']
graphTable['Outcome'] = graphTable.apply(func, axis = 1)
print '.'
graphTable = graphTable[['Player1','Player2','Outcome']]
print '.'
toAppend = graphTable[(graphTable.Outcome == 'V') | (graphTable.Outcome == 'L')  ]
print '.'
toAppend['Outcome'] = toAppend.apply(func2,axis = 1)
print '.'
toAppend.columns = ['Player2','Player1','Outcome']
print '.'
graphTable = graphTable.append(toAppend)

del toAppend
print '.'

graphTable['Count'] = 1

graphTable = graphTable.groupby(['Player1','Player2','Outcome'],as_index=False).count()

# del victoryTable
# del drawTable
# del lostTable
# del secondVictoryTable
# del secondLostTable

print '.'

OneIntermediate = pd.merge(graphTable,graphTable, left_on = 'Player2', right_on = 'Player1')[['Player1_x','Player2_y','Outcome_x','Outcome_y','Count_x','Count_y']]
OneIntermediate['Outcome'] = OneIntermediate[['Outcome_x','Outcome_y']].apply(lambda x : x[0] + x[1], axis = 1)
OneIntermediate = OneIntermediate[['Player1_x','Player2_y','Outcome','Count_x','Count_y']]
OneIntermediate['Count'] = OneIntermediate[['Count_x','Count_y']].apply(lambda x : x[0] * x[1], axis = 1)
OneIntermediate = OneIntermediate[['Player1_x','Player2_y','Outcome','Count']]
OneIntermediate.columns = ['Player1','Player2','Outcome','Count']
OneIntermediate = OneIntermediate[OneIntermediate.Player1 != OneIntermediate.Player2]
OneIntermediate = OneIntermediate.groupby(['Player1','Player2','Outcome'],as_index=False).count()

print '.'

TwoIntermediate = pd.merge(OneIntermediate,graphTable, left_on = 'Player2', right_on = 'Player1')[['Player1_x','Player2_y','Outcome_x','Outcome_y','Count_x','Count_y']]
TwoIntermediate['Outcome'] = TwoIntermediate[['Outcome_x','Outcome_y']].apply(lambda x : x[0] + x[1], axis = 1)
TwoIntermediate = TwoIntermediate[['Player1_x','Player2_y','Outcome','Count_x','Count_y']]
TwoIntermediate['Count'] = TwoIntermediate[['Count_x','Count_y']].apply(lambda x : x[0] * x[1], axis = 1)
TwoIntermediate = TwoIntermediate[['Player1_x','Player2_y','Outcome','Count']]
TwoIntermediate.columns = ['Player1','Player2','Outcome','Count']
TwoIntermediate = TwoIntermediate[TwoIntermediate.Player1 != TwoIntermediate.Player2]
TwoIntermediate = TwoIntermediate.groupby(['Player1','Player2','Outcome'],as_index=False).count()
print '.'

graphTable = graphTable.append(OneIntermediate.append(TwoIntermediate))
print '.'

values = pd.read_csv('validation.csv')[['WhitePlayer','BlackPlayer']]
values.columns = ['Player1','Player2']
print '.'

graphTable = pd.merge(graphTable, values, on = ['Player1','Player2'])
print '.'

# print TwoIntermediate
# print OneIntermediate
graphTable = graphTable.pivot_table(index=['Player1','Player2'], columns='Outcome', values='Count')
graphTable = graphTable.reset_index()
print '.'


graphTable.to_csv('LocalPropertiesWithPandas.csv')
print '.'



