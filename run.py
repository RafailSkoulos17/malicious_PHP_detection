import os
from time import time

from sklearn.model_selection import StratifiedKFold

from machine_learning import preprocess
from machine_learning.sgd.run_sgd import sgd_run
from machine_learning.svm.run_svm import svm_run
from machine_learning.decision_tree.run_decision_tree import decision_tree_run


def evaluate():

    input_file = os.path.join("outputs", "features", "function_and_human_readable_features.json")
    X, y = preprocess.get_features_and_labels(input_file)
    skf = StratifiedKFold(n_splits=5, random_state=42)
    splits = list(skf.split(X, y))
    svm_run(X, y, splits)
    decision_tree_run(X, y, splits)
    for loss in ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']:
        sgd_run(X, y, splits, loss)


if __name__ == '__main__':
    start = time()
    evaluate()
    print "Time in seconds: %.2f" % (time() - start)
