import numpy as np
from sklearn import svm
import os
import re


def read_files(target, dictionary):
    i = 1
    folders = os.listdir()
    for folder in folders:
        # spams
        if folder == "spam":
            spams = os.listdir("spam")
            for spam in spams:
                with open(folder+"/"+spam, "r", encoding="ISO-8859-1") as f:
                    content = f.read()
                    target.write("1 ")
                    for line in content.splitlines():
                        if line != "":
                            for word in re.split(",|\"| |\.", line):
                                mword = word.lower().strip()
                                if mword != '':
                                    if mword not in dictionary.values():
                                        dictionary[i] = mword
                                        target.write(str(i) + ": 1 ")
                                        i += 1
                                    else:
                                        k = check_dictionary(dictionary, mword)
                                        if (k):
                                            target.write(str(k) + ": 1 ")
                    target.write("\n")
        # not spams
        if folder == "nspam":
            nspams = os.listdir("nspam")
            for nspam in nspams:
                with open(folder+"/"+nspam, "r", encoding="ISO-8859-1") as f:
                    content = f.read()
                    target.write("0 ")
                    for line in content.splitlines():
                        if line != " ":
                            for word in re.split(",|\"| |\.", line):
                                mword = word.lower().strip()
                                if mword != '':
                                    if mword not in dictionary.values():
                                        dictionary[i] = mword
                                        target.write(str(i) + ": 1 ")
                                        i += 1
                                    else:
                                        k = check_dictionary(dictionary, mword)
                                        if (k):
                                            target.write(str(k) + ": 1 ")
                    target.write("\n")
    return dictionary


def check_dictionary(dictionary, word):
    for key in dictionary.keys():
        if (word == dictionary[key]):
            return key

    return False


target = open("test.txt", "w")
dictionary = {}
x = read_files(target, dictionary)
# dictionary_text = open("dictionary.txt", "w")
# dictionary_text.write(str(x))
# dictionary_text.close()
target.close()
C = 1.0  # SVM regularization parameter
svc = svm.SVC(kernel='linear', C=C)

y_predict = svc.predict(open("test.txt", "r").read())
print(y_predict)
