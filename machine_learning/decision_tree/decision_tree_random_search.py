import os
import operator
import xlwt
from machine_learning import preprocess
from machine_learning.geometric_mean import geometric_mean
from sklearn.metrics import make_scorer, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedShuffleSplit, RandomizedSearchCV, train_test_split, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier


def report(results):

    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Decision Tree")

    sheet1.write(0, 0, "Criterion")
    sheet1.write(0, 1, "Min samples split")
    sheet1.write(0, 2, "Max depth")
    sheet1.write(0, 3, "Min samples leaf")
    sheet1.write(0, 4, "Max leaf nodes")
    sheet1.write(0, 5, "Splitter")
    sheet1.write(0, 6, "Max features")
    sheet1.write(0, 7, "Class weight")

    sheet1.write(0, 8, "Precision")
    sheet1.write(0, 9, "Recall")
    sheet1.write(0, 10, "F1-score")
    sheet1.write(0, 11, "Geometric mean")

    criterion = results['param_criterion']
    max_depth = results['param_max_depth']
    max_leaf_nodes = results['param_max_leaf_nodes']
    min_samples_leaf = results['param_min_samples_leaf']
    min_samples_split = results['param_min_samples_split']
    splitter = results['param_splitter']
    max_features = results['param_max_features']
    class_weight = results['param_class_weight']

    f1 = map(lambda x: round(x, 2), results['mean_test_f1'])
    precision = map(lambda x: round(x, 2), results['mean_test_precision'])
    recall = map(lambda x: round(x, 2), results['mean_test_recall'])
    geometric_mean = map(lambda x: round(x, 2), results['mean_test_geometric_mean'])

    zipped_results = zip(criterion, min_samples_split, max_depth,
                         min_samples_leaf, max_leaf_nodes, splitter,
                         max_features, class_weight, precision,
                         recall, f1, geometric_mean)
    zipped_results = sorted(zipped_results, key=operator.itemgetter(10), reverse=True)[:20]

    for index, result in enumerate(zipped_results):
        sheet1.write(index+1, 0, result[0])
        sheet1.write(index+1, 1, result[1])
        sheet1.write(index+1, 2, result[2])
        sheet1.write(index+1, 3, result[3])
        sheet1.write(index+1, 4, result[4])
        sheet1.write(index+1, 5, result[5])
        sheet1.write(index+1, 6, result[6])
        sheet1.write(index+1, 7, str(result[7]))
        sheet1.write(index+1, 8, result[8])
        sheet1.write(index+1, 9, result[9])
        sheet1.write(index+1, 10, result[10])
        sheet1.write(index+1, 11, result[11])

    book.save(os.path.join("outputs", "results", "train", "Decision_tree_train_results.xls"))

    return [x[:8] for x in zipped_results]

def decision_tree_randomized_search(X, y):


    f1_scorer = make_scorer(f1_score, average='binary', pos_label=-1)
    precision_scorer = make_scorer(precision_score, average='binary', pos_label=-1)
    recall_scorer = make_scorer(recall_score, average='binary', pos_label=-1)
    gmean_scorer = make_scorer(geometric_mean)
    cv = StratifiedKFold(n_splits=4, random_state=42)
    param_dist = {"criterion": ["gini", "entropy"],
                  "min_samples_split": range(2, 21),
                  "max_depth": range(2, 21),
                  "min_samples_leaf": range(2, 21),
                  "max_leaf_nodes": range(2, 21),
                  "splitter": ["best", "random"],
                  "max_features": ["auto", "sqrt", "log2", None],
                  "class_weight": [{1: 1, -1: 1}, {1: 1, -1: 5}, {1: 1, -1: 10},
                                   {1: 1, -1: 15}, {1: 1, -1: 20}, 'balanced']
                  }

    n_iter_search = 100
    random_search = RandomizedSearchCV(DecisionTreeClassifier(), param_distributions=param_dist,
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
    _ = decision_tree_randomized_search(X, y)

