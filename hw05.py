import numpy as np
from sklearn import svm
import os
import re

def read_files():
    folders = os.listdir()
    spam_array = []
    for folder in folders:
        # spams
        if folder == "spam":
            spam_words = {}
            spams = os.listdir("spam")
            for spam in spams:
                with open(folder+"/"+spam, "r") as f:
                    content = f.read()
                    for line in content.splitlines():
                        if line != "":
                            for word in re.split(",|\"| |\.", line):
                                if word not in spam_words and word != " ":
                                    spam_words[word] = 1
        # not spams
        if folder == "nspam":
            nspam_words = {}
            nspams = os.listdir("nspam")
            for nspam in nspams:
                with open(folder+"/"+nspam, "r") as f:
                    content = f.read()
                    for line in content.splitlines():
                        if line != "":
                            for word in re.split(",|\"| |\.", line):
                                if word not in nspam_words and word != " ":
                                    nspam_words[word] = 1
    return [spam_words, nspam_words]

x = read_files()
print(x[0])
# clf = svm.SVC()
# clf.fit(list(x.values()), [0, 1])
