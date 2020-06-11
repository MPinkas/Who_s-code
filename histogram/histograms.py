from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from  sklearn.model_selection import  train_test_split
from sklearn.linear_model import LassoLarsIC
import shlex
import re
import os


class HistogramClassifier:

    def __init__(self):
        X,y=make_dataframe(letter_list)
        self.columns=list(X.columns)
        self.classifier=LassoLarsIC()
        self.classifier.fit(X,y)

    def predict(self,X):
        counter=snippet_to_histogram(X,letter_list)
        df=pd.DataFrame(columns=self.columns)
        df = df.append(counter, ignore_index=True).fillna(0)
        y=np.zeros(len(X))
        for i in range(len(X)):
            y[i]=self.classifier.predict(df)
        y=round(y.sum()/len(X))
        return y

def data_to_histogram(data, line_func):
    """
    :param data - the text file
    :param line_func - the function you want to use on a line
    :return histogram made from the text file
    """
    text_counter = Counter()
    with open(data) as f:
        for line in f:
            line_counter = Counter(line_func(line))
            text_counter += line_counter
    return text_counter


def word_list(line):
    """"
    :param line - string
    :return a array with all the words inside line
    """
    return re.sub("[^\w]", " ", line).split()


def letter_list(line):
    """"
    :param line - string
    :return a array with all the letters inside line
    """
    return list(line)


def word_histogram(data, i=0):
    """"
    :param i: 0 if data is text file everthing else its a array string
    :param data - text file
    :return a histogram from all the words inside data
    """
    if i == 0:
        return data_to_histogram(data, word_list)
    else:
        return snippet_to_histogram(data, word_list)


def letter_histogram(data, i=0):
    """"
    :param i: 0 if data is text file everthing else its a array string
    :param data - text file
    :return a histogram from all the letters inside data
    """
    if i == 0:
        return data_to_histogram(data, letter_list)
    else:
        return snippet_to_histogram(data, letter_list)


def snippet_to_histogram(data, line_func):
    """
    :param data - the string array
    :param line_func - the function you want to use on a line
    :return histogram made from the string array
    """
    columns=[]
    text_counter = Counter()
    for line in data:
        line_counter = Counter(line_func(line))
        text_counter += line_counter

    return text_counter


__location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
def histogram_dataframe(data, line_func):
    """"
    :param data - txt file name
    :param line_func the func that sould be used on data
    :return a dataframe containing the histogram of each
    """
    words = []
    counter_lines = []
    print(os.path.join(__location__, data))
    with open(os.path.join(__location__, data), "r", encoding="utf-8") as f:
        for line in f:
            line_array = line_func(line)
            for word in line_array:
                if word not in words:
                    words.append(word)
            if line_array:
                counter_lines.append(Counter(line_array))
    df = pd.DataFrame(columns=words)
    df = df.append(counter_lines,ignore_index=True).fillna(0)
    return df.astype(int)

def data_to_histograms(datas, y_values, line_func,drop_sum):
    """"
    :param datas - txt files name array
    :param y_values - the label value
    :param line_func - line_func the func that sould be used on data
    :param drop_sum - if the number of times a colum apper is less than drop_sum drop it
    :return a data frame made of lines from all  txt files
    """
    labels=[]
    dfs = []
    for i in range(len(y_values)):
        df = histogram_dataframe(datas[i], line_func)
        if drop_sum!=0:
            test=df.sum(axis=0)
            test=test.where(test<=drop_sum)
            test=test.dropna()
            df=df.drop(test.index,axis=1)
            test = df.sum(axis=1)
            test = test.where(test == 0)
            test = test.dropna()
            df = df.drop(test.index, axis=0)
        labels+=([y_values[i]]*df.shape[0])
        dfs.append(df)
    result = pd.concat(dfs, sort=False).reset_index().fillna(0)
    return result,labels



def make_dataframe(line_func,drop_sum=0):
    """"
    :param line_func - line_func the func that sould be used on data
    :param drop_sum - if the number of times a colum apper is less than drop_sum drop it
    :return a data frame made of lines from all  txt files given
    """
    datas = ["building_tool_all_data.txt", "espnet_all_data.txt", "horovod_all_data.txt", "jina_all_data.txt","PaddleHub_all_data.txt", "PySolFC_all_data.txt", "pytorch_geometric_all_data.txt"]
    #datas = ["building_tool_all_data.txt", "espnet_all_data.txt", "horovod_all_data.txt", "jina_all_data.txt","PaddleHub_all_data.txt", "PySolFC_all_data.txt", "pytorch_geometric_all_data.txt"]
    y_values = [0, 1, 2, 3, 4, 5, 6]
    #y_values = [0, 1, 2, 3, 4, 5, 6]
    return data_to_histograms(datas, y_values, line_func,drop_sum)


def main(counter):
    """"
    for testing
    """
    labels, values = zip(*Counter(counter).items())
    indexes = np.arange(len(labels))
    width = 1
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()

#works make_dataframe(letter_list)
if __name__ == "__main__":
    a=HistogramClassifier()
    print(a.predict(["    py_tag = PY37 \n",
"else:\n" ,
"    raise OSError('Jina requires Python 3.7 and above, but yours is %s' % sys.version)\n"]))