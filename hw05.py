# import numpy as np
from sklearn import svm
from sklearn.datasets import load_svmlight_file
import os
import re
import collections


def read_files(target, dictionary):
    i = 1
    folders = os.listdir()
    ordered_spam = []
    ordered_nspam = []
    for folder in folders:
        # spams
        if folder == "spam":
            spams = os.listdir("spam")
            for spam in spams:
                spam_dict = {}
                with open(folder+"/"+spam, "r", encoding="ISO-8859-1") as f:
                    content = f.read()
                    # target.write("1 ")
                    for line in content.splitlines():
                        if line != "":
                            for word in re.split(",|\"| |\.", line):
                                mword = word.lower().strip()
                                if mword != '':
                                    if mword not in dictionary.values():
                                        dictionary[i] = mword
                                        spam_dict[i] = 1
                                        # target.write(str(i) + ":1 ")
                                        i += 1
                                    else:
                                        k = check_dictionary(dictionary, mword)
                                        if (k):
                                            spam_dict[k] = 1
                                            # target.write(str(k) + ":1 ")

                    ordered_spam.append(collections.OrderedDict(sorted(spam_dict.items())))
                    # target.write("\n")
        # not spams
        if folder == "nspam":
            nspams = os.listdir("nspam")
            for nspam in nspams:
                nspam_dict = {}
                with open(folder+"/"+nspam, "r", encoding="ISO-8859-1") as f:
                    content = f.read()
                    # target.write("0 ")
                    for line in content.splitlines():
                        if line != " ":
                            for word in re.split(",|\"| |\.", line):
                                mword = word.lower().strip()
                                if mword != '':
                                    if mword not in dictionary.values():
                                        dictionary[i] = mword
                                        nspam_dict[i] = 1
                                        # target.write(str(i) + ":1 ")
                                        i += 1
                                    else:
                                        k = check_dictionary(dictionary, mword)
                                        if (k):
                                            nspam_dict[k] = 1
                                            # target.write(str(k) + ":1 ")
                    ordered_nspam.append(collections.OrderedDict(sorted(nspam_dict.items())))
                    # target.write("\n")
    return [ordered_spam, ordered_nspam]


def check_dictionary(dictionary, word):
    for key in dictionary.keys():
        if (word == dictionary[key]):
            return key

    return False


target = open("test.txt", "w")
dictionary = {}
x = read_files(target, dictionary)

#spam
for arr in x[0]:
    target.write("-1 ")
    for key, value in arr.items():
        target.write(str(key) + ":" + str(value) + " ")
    target.write("\n")

# not spam
for arr in x[1]:
    target.write("1 ")
    for key, value in arr.items():
        target.write(str(key) + ":" + str(value) + " ")
    target.write("\n")

target.close()
C = 1.0  # SVM regularization parameter
data = load_svmlight_file("test.txt")
svc = svm.SVC(kernel='linear', C=C)
print(svc.fit(data[0], data[1]))
# y_predict = svc.predict()
# print(y_predict)
