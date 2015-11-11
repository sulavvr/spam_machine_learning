# import numpy as np
from sklearn import svm
from sklearn.datasets import load_svmlight_file
import os
import re
import collections


def read_files():
    dictionary = {}
    i = 1
    folders = os.listdir('.')
    ordered_spam, ordered_nspam = [], []
    ordered_test = []
    for folder in folders:
        # spams
        if folder == 'spam':
            spams = os.listdir('spam')
            for spam in spams:
                spam_dict = {}
                with open(folder+'/'+spam, 'r', encoding='ISO-8859-1') as f:
                    content = f.read()
                    for line in content.splitlines():
                        if line != '':
                            for word in re.split(',|\"| |\.', line):
                                mword = word.lower().strip()
                                if mword != '':
                                    if mword not in dictionary.values():
                                        dictionary[i] = mword
                                        spam_dict[i] = 1
                                        i += 1
                                    else:
                                        dict_key = check_dictionary(dictionary, mword)
                                        if dict_key:
                                            spam_dict[dict_key] = 1
                    ordered_spam.append(collections.OrderedDict(sorted(spam_dict.items())))
        # not spams
        if folder == 'nspam':
            nspams = os.listdir('nspam')
            for nspam in nspams:
                nspam_dict = {}
                with open(folder+'/'+nspam, 'r', encoding='ISO-8859-1') as f:
                    content = f.read()
                    for line in content.splitlines():
                        if line != ' ':
                            for word in re.split(',|\"| |\.', line):
                                mword = word.lower().strip()
                                if mword != '':
                                    if mword not in dictionary.values():
                                        dictionary[i] = mword
                                        nspam_dict[i] = 1
                                        i += 1
                                    else:
                                        dict_key = check_dictionary(dictionary, mword)
                                        if dict_key:
                                            nspam_dict[dict_key] = 1
                    ordered_nspam.append(collections.OrderedDict(sorted(nspam_dict.items())))
        if folder == 'test':
            tests = os.listdir('test')
            for test in tests:
                test_dict = {}
                with open(folder+'/'+test, 'r', encoding='ISO-8859-1') as f:
                    content = f.read()
                    for line in content.splitlines():
                        if line != ' ':
                            for word in re.split(',|\"| |\.', line):
                                mword = word.lower().strip()
                                if mword != '':
                                    if mword not in dictionary.values():
                                        # dictionary[i] = mword
                                        # test_dict[i] = 1
                                        i += 1
                                    else:
                                        dict_key = check_dictionary(dictionary, mword)
                                        if dict_key:
                                            test_dict[dict_key] = 1
                    ordered_test.append(collections.OrderedDict(sorted(test_dict.items())))
    return [ordered_spam, ordered_nspam, dictionary, ordered_test]


def check_dictionary(word_dictionary, word):
    for k in word_dictionary.keys():
        if word == word_dictionary[k]:
            return k

    return False

target = open('train.txt', 'w', encoding='ISO-8859-1')
spam, not_spam, dictionary_words, test_arr = read_files()

max_key = 0
t = open('test.txt', 'w',  encoding='ISO-8859-1')
for arr in test_arr:
    t.write('0 ')
    for key, value in arr.items():
        t.write(str(key) + ':' + str(value) + ' ')
        if max_key < key:
            max_key = key
    t.write('\n')
t.close()

# spam
for arr in spam:
    target.write('-1 ')
    for key, value in arr.items():
        if key <= max_key:
            target.write(str(key) + ':' + str(value) + ' ')
    target.write('\n')

# not spam
for arr in not_spam:
    target.write('1 ')
    for key, value in arr.items():
        if key <= max_key:
            target.write(str(key) + ':' + str(value) + ' ')
    target.write('\n')

target.close()

dictionary_file = open('dictionary.txt', 'w',  encoding='ISO-8859-1')
for key, value in dictionary_words.items():
    dictionary_file.write(str(key) + ': ' + str(value) + '\n')
dictionary_file.close()

C = 1.0  # SVM regularization parameter
x_train, y_train = load_svmlight_file('train.txt')
svc = svm.SVC(kernel='linear', C=C)
svc.fit(x_train, y_train)

test_data = load_svmlight_file('test.txt')
predict = svc.predict(test_data[0])
print(predict)
# print(svc.score(data[0], data[1]))
