## CS224W-project

- There are three data folders: data, ranking and prediction. Please put all the csv files you generated into one of these folders.
- Each method/algorithm should output the predicted label file (see the format in prediction folder)
- All the results will be run in main.py
- If a method outputs rating for each player, use output_prediction function to return a predicted label file (See example in main.py)


## Update Results here
| Method         | Mean Abs Error | Exact Error | Balanced Error  |
| -------------  |:-------------: | -----------:|----------------:|
| Baseline       | 0.419  | 0.433      | 0.388 |
| Initial Rating | 0.403       |   0.392       | 0.402 |
| Pagerank Weighted  | 0.371       |   0.483       | 0.322 |
| Pagerank Weighted Tiebreak | 0.322       |   0.464      | 0.476 |


