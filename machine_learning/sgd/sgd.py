import os

import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, average_precision_score, f1_score, precision_score, recall_score
from sklearn import tree, preprocessing
from sklearn.model_selection import StratifiedShuffleSplit
from machine_learning import preprocess

input_file = os.path.join("outputs", "features", "function_and_human_readable_features.json")
X, y = preprocess.get_features_and_labels(input_file)

skf = StratifiedShuffleSplit(n_splits=10, test_size=0.3)
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
for train_index, test_index in skf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    std_scale = preprocessing.StandardScaler().fit(X_train)
    X_train = std_scale.transform(X_train)
    X_test = std_scale.transform(X_test)

    # X_train, X_test, y_train, y_test = train_test_split( feature_array, label_array, test_size = 0.3,stratify=label_array, random_state = 100)
    clf = SGDClassifier(loss="perceptron", penalty="l2",random_state=100, class_weight='balanced')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # accuracy = accuracy + accuracy_score(y_test, y_pred)*100

    precision_mal = precision_mal + precision_score(y_test, y_pred, average="binary", pos_label=-1)*100
    # precision_ben = precision_ben + precision_score(y_test, y_pred, average="binary", pos_label=1)*100
    # precision_avg = precision_avg + precision_score(y_test, y_pred, average="weighted", labels=[1, -1])*100

    recall_mal = recall_mal + recall_score(y_test, y_pred, average="binary", pos_label=-1)*100
    # recall_ben = recall_ben + recall_score(y_test, y_pred, average="binary", pos_label=1)*100
    # recall_avg = recall_avg + recall_score(y_test, y_pred, average="weighted", labels=[1, -1])*100

    f1_mal = f1_mal + f1_score(y_test, y_pred, average='binary', pos_label=-1)*100
    # f1_ben = f1_ben + f1_score(y_test, y_pred, average='binary', pos_label=1)*100
    # f1_avg = f1_avg + f1_score(y_test, y_pred, average="weighted", labels=[1, -1])*100

# print "Accuracy is ", accuracy/10

print "Precision for Malicious is", precision_mal/10
# print "Precision for Bening is", precision_ben/10
# print "Average Weighted Precision  is", precision_avg/10

print "Recall for Malicious is", recall_mal/10
# print "Recall for Bening is", recall_ben/10
# print "Average Weighted Recall is", recall_avg/10

print "F1 Score for Malicious is ", f1_mal/10
# print "F1 Score for Bening is ", f1_ben/10
# print "Average Weighted F1 Score is ", f1_avg/10
