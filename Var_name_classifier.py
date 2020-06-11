import re
import numpy as np

class NameClassifier:

    def __init__(self):
        return

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

    def _collect_var_names(self, X):

        for sample in X:
            pass

    def _sample_var_names(self, sample):
        """
        given a sample snippet (str) returns a list a variable names in it
        *may not return all names*

        Parameters
        ----------
        :param sample:
        :return:
        """
        def clean_end(line):
            """removes any subscription from a variable in a line ending in a variable
            (i.e. self.x[i] -> self.x)"""
            i = len(line) - 1
            ops = ['/','*','+','-','%']
            if any(op == line[i][-1] for op in ops):
                if len(line[i]) == 1:
                    return clean_end(line[:-1])
                line[i] = line[i][:-1]
                return clean_end(line)
            if ']' in line[i]:
                while i >= 0:
                    if '[' in line[i]:
                        break
                    i -= 1
                j = line[i].find('[')
                if j == 0:
                    i -= 1
                    return line[i]
                return line[i][:j]

            return line[i]

        def clean_str(line):
            """returns a variable from a line (provided it actually has one)"""
            dirty_var = clean_end(line)
            split_var = dirty_var.split('.')
            if len(split_var) == 0:  # in case variable name has self in it
                return split_var[0]
            if 'self' in split_var[0]:  # this is a local variable
                return split_var[1]
            return split_var[0]
            # note that this method throws away possible variable names but they could be named by other creators
            # for example the arr.shape, shape is not given by people who use numpy

        def clean_in_line(line):

            if line[-1][0].isnumeric():
                return ""

            if line[-1][0] == '-':
                line[-1] = line[-1][1:]
                return clean_in_line(line)

            if line[-1][-1] == ')':
                # in case of a function call or an operation of some sort which is too complex for right now
                return ""
            if line[-1][0] in ['\'', '\"']:
                # the thing before in is a string
                return ""

            return clean_str(line)
        # problems with the "in" variable name finder - could run into trouble for operations
        # commas are ignored (thus if we have a,b = foo() or a,b in zip(x,y) variable extract is a,b

        var = set()

        # checks for variable named before '=' (or == ??)
        edited_sample = sample.replace("==", "zzz") # avoid issues where == can have a non-variable before it
        equal_split = edited_sample.split("=")
        for i in range(len(equal_split) - 1):
            line = equal_split[i].split()
            temp = clean_str(line)
            var.add(temp)

        # checks for variables before in keyword
        in_split = sample.split(" in ")  # we dont want to accidentally break words
        for i in range(len(in_split) - 1):
            line = in_split[i].split()
            temp = clean_in_line(line)
            if temp == "":
                continue

        return
