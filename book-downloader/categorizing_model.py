import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import ConfusionMatrixDisplay

# load the directory where all book files are stored
filename = os.getcwd() + '\\booksLemma\\'

# set up list to store all files
filelist = []

# go through all files in the directory/subdirectories and append file addresses to a list
for root, dirs, files in os.walk(filename):
	for file in files:
        #append the file name to the list
		filelist.append(os.path.join(root,file))

# create two lists to store our text files
listTextFiles = []
listFileNames = []

# load every .txt file into a list
for fileName in filelist:

    catNumber = fileName[(fileName.rfind('\\') + 1):]
    catNumber = catNumber[:(catNumber.rfind('_'))]
    listFileNames.append(catNumber)

    with open(fileName, 'r', encoding="utf-8") as f:

        listTextFiles.append(str(f.read().rstrip()))

# turn into dataframe and make sure catalog number is an int
dictionaryFileLists = {'CatNum':listFileNames,'Document':listTextFiles}
textDF = pd.DataFrame(dictionaryFileLists)
textDF['CatNum']=textDF['CatNum'].astype(int)

# get labels from label file and make them a dataframe, again make sure catalog number is an int
filename = os.getcwd() + '\\BookTags.csv'
bookLabels = pd.read_csv(filename)
bookLabels['CatNum']=bookLabels['CatNum'].astype(int)

# merge the two dataframes, dropping any item that does not match on catelog number
inputDF = pd.merge(
    textDF,
    bookLabels,
    how="inner",
    left_on="CatNum",
    right_on="CatNum",)

# drop the catelog number since we no longer need it
inputDF.drop('CatNum', axis=1, inplace=True)

# use the below line of code to randomly drop 79% of the Fiction category, thus making it as large as the second largest category
#inputDF = inputDF.drop(inputDF.query('Tag =="Fiction"').sample(frac=.79).index)

# assign dataframe columns to lists of observations and labels
X = inputDF['Document'].tolist()
y = inputDF['Tag'].tolist()

# set up pipeline for predictive model
randfor = Pipeline([('vect', CountVectorizer(max_df = .65, min_df = 10)), # ,stop_words='english'
                    ('tfidf', TfidfTransformer()),
                    ('clf', svm.LinearSVC()),
                    ])

# run the model for prediciton using cross validation
y_pred = cross_val_predict(randfor, X, y, cv=10)

# print a confusion matrix of the model predictions
conf_mat = confusion_matrix(y, y_pred)
print(conf_mat)

# export a pretty confusion matrix of the model predictions
ConfusionMatrixDisplay.from_predictions(y, y_pred)
font = {'family' : 'normal',
    'size'   : 19}
plt.rc('font', **font)
plt.show()

# print the accuracy scores
print ("accuracy", accuracy_score(y, y_pred))
print(f1_score(y, y_pred, zero_division=1, average = 'weighted'))