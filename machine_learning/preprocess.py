import inspect
import os
import sys
import json
import math
import copy
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

SRC_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_features_and_labels(input_file):
    with open(os.path.join(SRC_DIR, input_file), "r") as f:
        feature_dict = json.load(f)
    index = feature_dict.keys()
    features = pd.DataFrame.from_dict(feature_dict, orient='index', dtype=None)

    labels_df = features.loc[:, 'label']
    features_df = features.drop('label', 1)

    labels = labels_df.values
    features = features_df.values
    return features, labels


    i = 1

    # malicious_dict = {}
    # bening_dict = {}
    #
    # my_dict = copy.deepcopy(feature_dict)
    # for filename, features in my_dict.iteritems():
    #     if features["label"] == -1:
    #         malicious_dict[filename] = features
    #         del malicious_dict[filename]["label"]
    #     else:
    #         bening_dict[filename] = features
    #         del bening_dict[filename]["label"]
    #
    # labels = {}
    # for filename, features in feature_dict.iteritems():
    #     labels[filename] = features["label"]
    #     del feature_dict[filename]["label"]
    #
    # label_array = pd.Series(labels).values
    #
    # feature_array = []
    # for filename, features in feature_dict.iteritems():
    #     temp = pd.Series(features)
    #     feature_array.append(temp.values)
    # feature_array = np.array(feature_array).astype('float64')
    #
    # malicious_array = []
    # for filename, features in malicious_dict.iteritems():
    #     temp = pd.Series(features)
    #     malicious_array.append(temp.values)
    #
    # rows, columns = feature_array.shape
    # malicious_mean_per_col = [0 for i in range(columns)]
    # for ind_row, row in enumerate(malicious_array):
    #     for ind_col, col in enumerate(row):
    #         if not math.isnan(col):
    #             malicious_mean_per_col[ind_col] += col
    # size = len(malicious_array)
    # malicious_mean_per_col = [float(x) / size for x in malicious_mean_per_col]
    #
    # bening_array = []
    # for filename, features in bening_dict.iteritems():
    #     temp = pd.Series(features)
    #     bening_array.append(temp.values)
    # bening_mean_per_col = [0 for i in range(columns)]
    # for ind_row, row in enumerate(bening_array):
    #     for ind_col, col in enumerate(row):
    #         if not math.isnan(col):
    #             bening_mean_per_col[ind_col] += col
    # size = len(bening_array)
    # bening_mean_per_col = [float(x) / size for x in bening_mean_per_col]
    #
    # #-------------Reppace null values------------------
    # inds = np.where(np.isnan(feature_array))
    # for row, col in zip(*inds):
    #     if label_array[row] == 1:
    #         feature_array[row,col] = bening_mean_per_col[col]
    #     else:
    #         feature_array[row,col] = malicious_mean_per_col[col]
    # X = feature_array
    # y = label_array
    #




    # plt.figure()
    # key, value = feature_dict.popitem()
    # df = pd.DataFrame(X, columns=[key2 for key2,value2 in value.iteritems()])
    # axes = pd.tools.plotting.scatter_matrix(df, alpha=0.2)
    # # plt.tight_layout()
    # plt.show()


    # key, value = feature_dict.popitem()
    # new =  np.zeros((285, 16))
    # new[:, :-1] = X
    # new[:, -1] = y
    # d = pd.DataFrame(new, columns=[key2 for key2, value2 in value.iteritems()].append("label"))
    # seaborn.pairplot(new, hue="label")

if __name__=='__main__':
    input_file = os.path.join("outputs", "features", "function_and_human_readable_features.json")
    get_features_and_labels(input_file)
