from Line_length_classfier import LineClassifier
import numpy as np
from collections import defaultdict


class ConsensusClassifier:
    """
    Consensus_classifier.py holds in it a list of classifiers and when trained trains them all and scores how good they
    are giving their predictions more or less weight

    classifiers working with this one must implement fit (not train) and predict
    (which returns a dict with keys being labels and values being floats in [0,1]
    (fit and predict signatures should match this classes fit and predicts  functions
    """
    def __init__(self):
        # in order to add more classifiers just import them up top and construct a new one and append to _classifiers
        # also append a 1 to _w
        self._classifiers = []
        self._w = []  # array of weights for each classifier
        self._classifiers.append(LineClassifier(5))
        self._w.append(1)

    def fit(self, X, y):
        """
        trains all given classifiers and weighs their voting power

        parameters
        ----------
        :param X: training data shape=(num_samples,) of strings
        :param y: training data labels shape=(num_samples,)
        """
        # consider splitting sampling data so scoring is done while compensating for overfitting
        for c in self._classifiers:
            c.fit(X, y)

        # consider scoring on less points to decrease runtime
        for i in range(len(self._classifiers)):
            self._w[i] = self._score(self._classifiers[i], X, y)

    def _score(self, classifier, X, y):
        """
        scores a classifier based on given data (assumes classifier implements predict and it returns a dict)

        parameters
        ----------
        :param classifier: some classifier that implements predict that returns a dict
        :param X: data, shape=(num_samples,) dtype=string
        :param y: labels, shape=(num_samples,)
        :return:
        """
        score = 0
        pred = classifier.predict(X)
        for i in range(y.shape[0]):
            if y[i] in pred[i].keys():
                score += pred[i][y[i]]
        return score

    def predict(self, X):
        """
        performs a prediction based on given classifiers consensus

        parameters
        ----------
        :param X: data, shape=(num_samples,) dtype=string
        :return: prediction array of shape=(num_samples,)
        """

        def _consensus(scores):
            best_score = -1  # promises best key will be changed since all scores are non-negative
            best_key = 0
            for key in scores.keys():
                if scores[key] > best_score:
                    best_score = scores[key]
                    best_key = key
            return key

        preds = []
        for i in range(len(self._classifiers)):
            preds.append(self._classifiers[i].predict(X))

        res = []
        for j in range(X.shape[0]):
            scores = defaultdict(float)
            for i in range(len(preds)):  # this loop isn't so bad since we will have <5 classifiers
                for key in preds[i].keys():  # and <7 keys
                    scores[key] += preds[i][key]
            res.append(_consensus(scores))

        return res
