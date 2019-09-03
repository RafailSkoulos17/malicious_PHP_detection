import numpy as np
from sklearn.metrics import confusion_matrix

def geometric_mean(y_pred, y_true, pos_label=None):
    # inds = []
    # if pos_label is not None:
    #     for ind, value in enumerate(y_true):
    #         if value != pos_label:
    #            inds.append(ind)
    # y_pred = np.delete(y_pred, inds)
    # y_true = np.delete(y_true, inds)
    tn, fp, fn, tp = confusion_matrix(y_pred, y_true).ravel()
    try:
        sensitivity = float(tp) / (tp + fn)
    except ZeroDivisionError:
        sensitivity = 0
    try:
        specificity =  float(tn) / (tn + fp)
    except ZeroDivisionError:
        specificity = 0
    gmean = (sensitivity * specificity) ** (0.5)
    return gmean

