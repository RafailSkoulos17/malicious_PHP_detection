import os
import numpy as np
import xlwt

from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from machine_learning import preprocess
from machine_learning.geometric_mean import geometric_mean
from machine_learning.svm.svm_random_search import svm_randomized_search


def svm_run(X, y, splits):
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
    sheet1.write(0, 9, "True Positive Rate")
    sheet1.write(0, 10, "False Positive Rate")
    sheet1.write(0, 11, "False Negative Rate")

    svm_params = svm_randomized_search(X, y)
    res = []

    with open(os.path.join("outputs", "results", "test", "svm_results.txt"), "w") as f:
        pass

    for index, result in enumerate(svm_params):
        kernel = result[0]
        C = result[1]
        gamma = result[2]
        class_weight = result[3]
        decision_function_shape = result[4]
        precision_list = []
        recall_list = []
        f1_list = []
        gmean_list = []
        TPR = []
        FPR = []
        FNR = []

        for train_index, test_index in splits:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            scaler = StandardScaler().fit(X_train)
            X_train_scaled = scaler.transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            clf = SVC(kernel=kernel, C=C, gamma=gamma,
                      class_weight=class_weight,
                      decision_function_shape=decision_function_shape,
                      random_state=42)
            clf.fit(X_train_scaled, y_train)
            y_pred = clf.predict(X_test_scaled)
            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

            TPR.append(round(float(tp) / (tp + fn), 2)) # also called specificity
            FPR.append(round(float(fp) / (fp + tn), 2))
            FNR.append(round(float(fn) / (tp + fn), 2))

            precision = round(precision_score(y_test, y_pred, average="binary", pos_label=-1), 2)
            precision_list.append(precision)

            recall = round(recall_score(y_test, y_pred, average="binary", pos_label=-1), 2)
            recall_list.append(recall)

            f1 = round(f1_score(y_test, y_pred, average="binary", pos_label=-1), 2)
            f1_list.append(f1)

            gmean = round(geometric_mean(y_test, y_pred), 2)
            gmean_list.append(gmean)

        TPR_mean = round(np.mean(TPR), 2)
        TPR_var = round(np.var(TPR) ** (0.5) * 2, 2)

        FPR_mean = round(np.mean(FPR), 2)
        FPR_var = round(np.var(FPR) ** (0.5) * 2, 2)

        FNR_mean = round(np.mean(FNR), 2)
        FNR_var = round(np.var(FNR) ** (0.5) * 2, 2)

        precision_mean = round(np.mean(precision_list), 2)
        precision_var = round(np.var(precision_list) ** (0.5) * 2, 2)

        recall_mean = round(np.mean(recall_list), 2)
        recall_var = round(np.var(recall_list) ** (0.5) * 2, 2)

        f1_mean = round(np.mean(f1_list), 2)
        f1_var = round(np.var(f1_list) ** (0.5) * 2, 2)

        gmean_mean = round(np.mean(gmean_list), 2)
        gmean_var = round(np.var(gmean_list) ** (0.5) * 2, 2)


        res.append([kernel, C, gamma, class_weight, decision_function_shape,
                    (precision_mean, precision_var), (recall_mean, recall_var),
                    (f1_mean, f1_var), (gmean_mean, gmean_var), (TPR_mean, TPR_var),
                    (FPR_mean, FPR_var), (FNR_mean, FNR_var)])

        with open(os.path.join("outputs", "results", "test", "svm_results.txt"), "a") as f:
            f.write("kernel={0}, C={1}, gamma={2}, class_weight={3}, decision_function_shape={4}\n".format(
                kernel, C, gamma, str(class_weight),decision_function_shape))
            f.write("PRECISION SCORES: {0}, PRECISION MEAN: {1}, PRECISION VARIANCE: {2}\n".format(str(precision_list),
                                                                                                   precision_mean,
                                                                                                   precision_var))
            f.write("RECALL SCORES: {0}, RECALL MEAN: {1}, RECALL VARIANCE: {2}\n".format(str(recall_list),
                                                                                          recall_mean,
                                                                                          recall_var))
            f.write("F1 SCORES: {0}, F1 MEAN: {1}, F1 VARIANCE: {2}\n".format(str(f1_list),
                                                                              f1_mean,
                                                                              f1_var))
            f.write("GEOMETRIC MEAN SCORES: {0}, GEOMETRIC MEAN MEAN: {1}, GEOMETRIC MEAN VARIANCE: {2}\n".format(
                                                                                        str(gmean_list),
                                                                                        gmean_mean,
                                                                                        gmean_var))
            f.write('TRUE POSITIVE RATE SCORES: {0},  TRUE POSITIVE RATE MEAN: {1}, TRUE POSITIVE RATE VARIANCE:'
                    ' {2}\n'.format(TPR, TPR_mean, TPR_var))

            f.write('FALSE POSITIVE RATE SCORES: {0},  FALSE POSITIVE RATE MEAN: {1}, FALSE POSITIVE RATE VARIANCE:'
                    ' {2}\n'.format(FPR, FPR_mean, FPR_var))

            f.write('FALSE NEGATIVE RATE SCORES: {0},  FALSE NEGATIVE RATE MEAN: {1}, FALSE NEGATIVE RATE VARIANCE:'
                    ' {2}\n'.format(FNR, FNR_mean, FNR_var))

            f.write("----------------------------------------------------------\n")

    # res = sorted(res, key=operator.itemgetter(7), reverse=True)

    for index, result in enumerate(res):
        sheet1.write(index+1, 0, result[0])
        sheet1.write(index+1, 1, result[1])
        sheet1.write(index+1, 2, result[2])
        sheet1.write(index+1, 3, str(result[3]))
        sheet1.write(index+1, 4, result[4])
        sheet1.write(index+1, 5, str(result[5]))
        sheet1.write(index+1, 6, str(result[6]))
        sheet1.write(index+1, 7, str(result[7]))
        sheet1.write(index+1, 8, str(result[8]))
        sheet1.write(index+1, 9, str(result[9]))
        sheet1.write(index+1, 10, str(result[10]))
        sheet1.write(index+1, 11, str(result[11]))

    book.save(os.path.join("outputs", "results", "test", "SVM_test_results.xls"))

if __name__ == '__main__':
    input_file = os.path.join("outputs", "features", "function_and_human_readable_features.json")
    X, y = preprocess.get_features_and_labels(input_file)
    skf = StratifiedKFold(n_splits=5, random_state=42)
    splits = list(skf.split(X, y))
    svm_run(X, y, splits)
