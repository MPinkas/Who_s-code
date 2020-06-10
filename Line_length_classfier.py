import numpy as np


class LineClassifier:

    def __init__(self, k):
        """
        constructor
        """
        self.trained = []
        self.labels = []
        self.k = k

    def fit(self, X, y):
        """
        trains the classifier based on input data

        parameters
        ----------
        :param X: training data, list of length num_samples, every entry is a string
        :param y: labels, shape=(num_samples)
        """
        labels = y
        trained = self._process_input(X)

        # order everything by values of _process_input for easier finding
        self.labels = [a for a in sorted(zip(trained, y))]
        self.trained = sorted(trained)
        zzz = 1

    def _process_input(self, X):
        """
        changes input strings into comparable keys

        parameters
        ----------
        :param X: training data, list of length num_samples, every entry is a string
        :return:
        """
        factor = [1, 10 ** 3, 10 ** 6, 10 ** 9, 10 ** 12]
        processed_X = []
        for sample in X:
            lines = sample.splitlines()
            key = 0
            # todo decide if empty lines are considered lines or not (through testing)
            for i in range(len(lines)):
                key += factor[i] * len(lines[i])
            processed_X.append(key)
        return processed_X

    def predict(self, X):

        p_X = self._process_input(X)
        for sample in p_X:
            pass

    def _single_nn(self, sample):
        """
        gets the k nearest neighbors to a given sample

        parameters
        ----------
        :param sample: int translation of given sample
        :return:
        """
        top = len(self.trained) - 1
        bot = 0

        if sample >= self.trained[top]:
            return self.trained[len(self.trained) - self.k:]
        if sample <= self.trained[0]:
            return self.trained[:self.k]

        # sort of binary search for nearest neighbor approx
        # (note that this is not distance based since ordering is done by number of lines first)
        while True:
            mid = int((top + bot) / 2)
            if self.trained[mid] > sample:
                top = mid
                if self.trained[mid - 1] <= sample:
                    mid -= 1
                    break
                continue
            if self.trained[mid] < sample:
                bot = mid
                if self.trained[mid + 1] >= sample:
                    break
                continue
            break  # sample == self.trained[mid]

        # finds k nearest neighbors (assumes k < size of trainig data)
        return self._get_knn(mid, sample)

    def _get_knn(self, mid, sample):
        """
        gets the k nearest neighbors of a sample given the 1 nearest neighbors index

        parameters
        ----------
        :param mid: nearest neighbor index
        :param sample: sample point (int)
        :return: list of k nearest neighbors
        """
        smaller = mid
        larger = mid + 1
        res = []
        while len(res) < self.k:
            if self._sample_dist(sample, self.trained[larger]) > \
                    self._sample_dist(sample, self.trained[smaller]):
                res.append(self.trained[smaller])
                smaller -= 1
                if smaller == -1:
                    break
            else:
                res.append(self.trained[larger])
                larger += 1
                if larger == len(self.trained):
                    break
        else:
            return res

        if smaller < 0:
            while len(res) < self.k:
                res.append(self.trained[larger])
                larger += 1
            return res

        while len(res) < self.k:
            res.append(self.trained[smaller])
            larger -= 1

        return res

    def _sample_dist(self, x, y):

        dist = 0
        d_x = x
        d_y = y
        while True:
            dist += abs((d_x % 1000) - (d_y % 1000))
            d_x //= 1000
            d_y //= 1000
            if d_x == 0 and d_y == 0:
                break
        return dist

    def score(self, X, y):
        pass
