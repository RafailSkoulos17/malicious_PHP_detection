import os
import operator
import xlwt
import numpy as np

from time import time

from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

from machine_learning import preprocess
from machine_learning.geometric_mean import geometric_mean
from sklearn.metrics import make_scorer, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedShuffleSplit, RandomizedSearchCV, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier


def report(results):

    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("SGD")

    sheet1.write(0, 0, "Loss")
    sheet1.write(0, 1, "Penalty")
    sheet1.write(0, 2, "Apha")
    sheet1.write(0, 3, "L1 ratio")
    sheet1.write(0, 4, "Learning rate")
    sheet1.write(0, 5, "Warm start")
    sheet1.write(0, 6, "Class weigtht")

    sheet1.write(0, 7, "Precision")
    sheet1.write(0, 8, "Recall")
    sheet1.write(0, 9, "F1-score")
    sheet1.write(0, 10, "Geometric mean")

    loss = results['param_loss']
    penalty = results['param_penalty']
    alpha = results['param_alpha']
    l1_ratio = results['param_l1_ratio']
    learning_rate = results['param_learning_rate']
    warm_start = results['param_warm_start']
    class_weight = results['param_class_weight']
    f1 = map(lambda x: round(x, 2), results['mean_test_f1'])
    precision = map(lambda x: round(x, 2), results['mean_test_precision'])
    recall = map(lambda x: round(x, 2), results['mean_test_recall'])
    geometric_mean = map(lambda x: round(x, 2), results['mean_test_geometric_mean'])

    zipped_results = zip(loss, penalty, alpha, l1_ratio, learning_rate, warm_start,
                         class_weight, precision, recall, f1, geometric_mean)
    zipped_results = sorted(zipped_results, key=operator.itemgetter(9), reverse=True)[:20]

    for index, result in enumerate(zipped_results):
        sheet1.write(index+1, 0, result[0])
        sheet1.write(index+1, 1, result[1])
        sheet1.write(index+1, 2, result[2])
        sheet1.write(index+1, 3, result[3])
        sheet1.write(index+1, 4, result[4])
        sheet1.write(index+1, 5, result[5])
        sheet1.write(index+1, 6, str(result[6]))
        sheet1.write(index+1, 7, result[7])
        sheet1.write(index+1, 8, result[8])
        sheet1.write(index+1, 9, result[9])
        sheet1.write(index+1, 10, result[10])

    book.save(os.path.join("outputs", "results", "train", "SGD_train_" + str(loss[0]) + "_results.xls"))
    return [x[:7] for x in zipped_results]



def sgd_randomized_search(X, y, loss):
    f1_scorer = make_scorer(f1_score, average='binary', pos_label=-1)
    precision_scorer = make_scorer(precision_score, average='binary', pos_label=-1)
    recall_scorer = make_scorer(recall_score, average='binary', pos_label=-1)
    gmean_scorer = make_scorer(geometric_mean)
    cv = StratifiedKFold(n_splits=4, random_state=42)

    scaler = StandardScaler().fit(X)
    X = scaler.fit_transform(X)
    param_dist = {"loss": [loss],
                  "penalty": ['l1', 'l2', 'elasticnet'],
                  "alpha": 10.0**-np.arange(1, 7),
                  "learning_rate": ["optimal"],
                  "warm_start": [True, False],
                  "l1_ratio": np.arange(0.15, 0.86, 0.05),
                  "class_weight": [{1: 1, -1: 1}, {1: 1, -1: 5}, {1: 1, -1: 10},
                                   {1: 1, -1: 15}, {1: 1, -1: 20}, 'balanced']
                  }

    n_iter_search = 100
    random_search = RandomizedSearchCV(SGDClassifier(), param_distributions=param_dist,
                                       n_iter=n_iter_search,
                                       scoring={'precision': precision_scorer, 'recall': recall_scorer,
                                                'f1': f1_scorer, 'geometric_mean': gmean_scorer},
                                       cv=cv, refit='f1', n_jobs=-1, random_state=42)

    random_search.fit(X, y)

    return report(random_search.cv_results_)

if __name__ == "__main__":
    print("-- Random Parameter Search via 4-fold CV")
    input_file = os.path.join("outputs", "features", "function_and_human_readable_features.json")
    X, y = preprocess.get_features_and_labels(input_file)
    for loss in ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']:
        _ = sgd_randomized_search(X, y, loss)

