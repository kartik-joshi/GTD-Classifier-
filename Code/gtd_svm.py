# -*- coding: utf-8 -*-
"""GTD_SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12bmG-aDBNxowLeyuG1aLZknKBxysOLq-
"""

from csv import reader
from sklearn import svm
import numpy as np
import time
from csv import reader

from google.colab import files
uploaded = files.upload()

# Read datasets from CSV input file
def Read_file(file_name):
    dataset = list()
    with open(file_name, 'r', newline='',encoding='utf-8') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset

# Convert string columns to float in input dataset
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

# Convert string column to integer in input dataset (last column with class value)
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup

# Find the min and max values for each column
def dataset_minmax(dataset):
    stats = [[min(column), max(column)] for column in zip(*dataset)]
    return stats

# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row) - 1):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])

# Input dataset
Data = Read_file('GTD_Data_2.csv')
Target = Read_file('GTD_Target_2.csv')

import numpy as np
def next_batch(num, data, labels):
    idx = np.arange(0 , len(data))
    np.random.shuffle(idx)
    idx = idx[:num]
    data_shuffle = [data[ i] for i in idx]
    labels_shuffle = [labels[ i] for i in idx]

    return np.asarray(data_shuffle), np.asarray(labels_shuffle)

Data, Target = next_batch(len(Data),Data,Target)
traindata = Data[0:70000]
traintarget = Target[0:70000]
testdata = Data[90000:]
testtarget = Target[90000:]

clf = svm.SVC(C=1.3,max_iter=3000,decision_function_shape='ovo')
clf.fit(traindata, traintarget)

#test network
count = 0
total  = 0
for i in range(0,len(testdata)):
    total +=1
    temp = clf.predict([testdata[i]])
    if temp == testtarget[i]:
        count+=1
accuracy = count*100/total
print('Accuracy: %s' % accuracy)