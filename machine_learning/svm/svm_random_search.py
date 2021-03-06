import os
import operator
import xlwt
import scipy

from machine_learning import preprocess
from machine_learning.geometric_mean import geometric_mean
from sklearn import svm
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import make_scorer, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedShuffleSplit, RandomizedSearchCV, StratifiedKFold


def report(results):

    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("SVM")

    sheet1.write(0, 0, "Kernel")
    sheet1.write(0, 1, "C")
    sheet1.write(0, 2, "Gamma")
    sheet1.write(0, 3, "Class weight")
    sheet1.write(0, 4, "Decision_function_shape")

    sheet1.write(0, 5, "Precision")
    sheet1.write(0, 6, "Recall")
    sheet1.write(0, 7, "F1-score")
    sheet1.write(0, 8, "Geometric mean")

    kernel = results['param_kernel']
    C = results['param_C']
    gamma = results['param_gamma']
    class_weight = results['param_class_weight']
    decision_function_shape = results['param_decision_function_shape']

    f1 = map(lambda x: round(x, 2), results['mean_test_f1'])
    precision = map(lambda x: round(x, 2), results['mean_test_precision'])
    recall = map(lambda x: round(x, 2), results['mean_test_recall'])
    geometric_mean = map(lambda x: round(x, 2), results['mean_test_geometric_mean'])

    zipped_results = zip(kernel, C, gamma, class_weight, decision_function_shape,
                         precision, recall, f1, geometric_mean)
    zipped_results = sorted(zipped_results, key=operator.itemgetter(7), reverse=True)[:20]

    for index, result in enumerate(zipped_results):
        sheet1.write(index+1, 0, result[0])
        sheet1.write(index+1, 1, result[1])
        sheet1.write(index+1, 2, result[2])
        sheet1.write(index+1, 3, str(result[3]))
        sheet1.write(index+1, 4, result[4])
        sheet1.write(index+1, 5, result[5])
        sheet1.write(index+1, 6, result[6])
        sheet1.write(index+1, 7, result[7])
        sheet1.write(index+1, 8, result[8])

    book.save(os.path.join("outputs", "results", "train", "SVM_train_results.xls"))
    return [x[:5] for x in zipped_results]


def svm_randomized_search(X, y):

    f1_scorer = make_scorer(f1_score, average='binary', pos_label=-1)
    precision_scorer = make_scorer(precision_score, average='binary', pos_label=-1)
    recall_scorer = make_scorer(recall_score, average='binary', pos_label=-1)
    gmean_scorer = make_scorer(geometric_mean)
    cv = StratifiedKFold(n_splits=4, random_state=42)

    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)

    kernels = ["rbf", "linear"]
    class_weight_range = [{1: 1, -1: x} for x in [1, 5, 10, 15, 20]] + ['balanced']
    param_dist = {'C': scipy.stats.expon(scale=100), 'gamma': scipy.stats.expon(scale=.1),
                  'kernel': kernels, 'class_weight': class_weight_range,
                  'decision_function_shape': ['ovo', 'ovr']}

    n_iter_search = 100
    random_search = RandomizedSearchCV(svm.SVC(), param_distributions=param_dist,
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
    _ = svm_randomized_search(X, y)




