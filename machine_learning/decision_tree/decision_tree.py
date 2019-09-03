import os
import sys
import inspect
import pprint
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE

from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2, SelectPercentile, f_classif
from sklearn.metrics import accuracy_score, average_precision_score, f1_score, precision_score, recall_score, \
    confusion_matrix

from sklearn import preprocessing
from scipy.sparse import issparse
from sklearn import svm, decomposition
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
from sklearn.tree import DecisionTreeClassifier

from machine_learning import preprocess
from machine_learning.geometric_mean import geometric_mean


input_file = os.path.join("outputs", "features", "function_and_human_readable_features.json")
print "Dataset: function_and_human_readable_features"
X, y = preprocess.get_features_and_labels(input_file)




accuracy = 0
precision_mal = 0
precision_ben = 0
precision_avg = 0
recall_mal = 0
recall_ben = 0
recall_avg = 0
f1_mal = 0
f1_ben = 0
f1_avg = 0
gmean = 0
f_scores = []

# X_dev, X_eval, y_dev, y_eval = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

sss = StratifiedShuffleSplit(n_splits=10, test_size=0.3, random_state=100)
# print 'Original dataset shape {}'.format(X.shape)
# sm = SMOTE(ratio='minority', kind='borderline1', k_neighbors=3, m_neighbors=10,
#            random_state=42, n_jobs=-1)
#
# X, y = sm.fit_sample(X, y)
# print 'Resampled dataset shape {}'.format(X.shape)

for train_index, test_index in sss.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    malicious_samples = len([1 for i in y_train if i == -1])
    benign_samples = len([1 for i in y_train if i == 1])
    print 'Original dataset shape {}'.format(X_train.shape)
    sm = SMOTE(ratio='minority', kind='borderline1', k_neighbors=3, m_neighbors=10,
               random_state=42, n_jobs=-1)

    X_train, y_train = sm.fit_sample(X_train, y_train)
    print 'Resampled dataset shape {}'.format(X_train.shape)

    std_scale = preprocessing.StandardScaler().fit(X_train)
    X_train = std_scale.transform(X_train)
    X_test = std_scale.transform(X_test)

    clf_entropy = DecisionTreeClassifier(criterion="entropy", random_state=100,
                                         max_depth=10, min_samples_leaf=5)
    clf_entropy.fit(X_train, y_train)
    y_pred = clf_entropy.predict(X_test)

    tn, fp, fn, tp = conf_matrix = confusion_matrix(y_test, y_pred).ravel()
    print "(TN, FP, FN, TP) = {}".format((tn, fp, fn, tp))

    gmean += geometric_mean(y_test, y_pred) * 100
    precision_mal += precision_score(y_test, y_pred, average="binary", pos_label=-1)*100
    recall_mal += recall_score(y_test, y_pred, average="binary", pos_label=-1)*100
    f1_mal += f1_score(y_test, y_pred, average='binary', pos_label=-1)*100
    f_scores.append(f1_score(y_test, y_pred, average='binary', pos_label=-1)*100)

    # accuracy = accuracy + accuracy_score(y_test,y_pred)*100
    # precision_ben = precision_ben + precision_score(y_test, y_pred, average="binary", pos_label=1)*100
    # precision_avg = precision_avg + precision_score(y_test, y_pred, average="weighted", labels=[1, -1])*100
    # recall_ben = recall_ben + recall_score(y_test, y_pred, average="binary", pos_label=1)*100
    # recall_avg = recall_avg + recall_score(y_test, y_pred, average="weighted", labels=[1, -1])*100
    # f1_ben = f1_ben + f1_score(y_test, y_pred, average='binary', pos_label=1)*100
    # f1_avg = f1_avg + f1_score(y_test, y_pred, average="weighted", labels=[1, -1])*100

# print "Accuracy is ", accuracy/10

print "TEST: Precision for Malicious is", precision_mal/10
# print "Precision for Bening is", precision_ben/10
# print "Average Weighted Precision  is", precision_avg/10

print "TEST: Recall for Malicious is", recall_mal/10
# print "Recall for Bening is", recall_ben/10
# print "Average Weighted Recall is", recall_avg/10

print "TEST: F1 Score for Malicious is ", f1_mal/10
# print "F1 Score for Bening is ", f1_ben/10
# print "Average Weighted F1 Score is ", f1_avg/10

print "TEST: Geometric mean is", gmean/10

f_scores = np.array(f_scores)
v = (np.var(f_scores) ** (0.5)) * 2

print "TEST: Variance is: {0}".format(v)
pprint.pprint(f_scores)


print '-----------------------------------------------------------------'
