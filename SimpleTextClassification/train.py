import os
import pandas as pd
import numpy as np
import pypyodbc
import re
from warnings import filterwarnings
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, auc
from sklearn.svm import LinearSVC

import pickle
from stringcleaner import clean_str
filterwarnings('ignore')


'''
Data format
____________________

STOP(column: text string)       |    catclass (column: class of text)
blah blah blah                  |     2
blah blah blah                  |     1     


'''

mainqry = """ """ #trainData

testQuery = """ """  #test data

cnxn = pypyodbc.connect(r"Driver={driver};"
                        "Server=server;"
                        "Database=database;"
                        "Trusted_Connection=yes")


maindf = pd.read_sql(mainqry, cnxn)
testdf = pd.read_sql(testQuery, cnxn)
cnxn.close()

x = []
for i in range(maindf.shape[0]):
    x.append(clean_str(str(maindf.iloc[i][0])))
y = np.array(maindf["catclass"])
y = np.char.mod('%d', y)


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3,stratify = y ,random_state=5)


model = Pipeline([('vectorizer',
                   CountVectorizer(
                       ngram_range=(1, 1),
                       strip_accents="ascii",
                       lowercase=True,
                       stop_words="english",
                       max_features=6000)),
                  ('tfidf', TfidfTransformer(use_idf=True)),
                  ('clf',LinearSVC(C=5.3, penalty='l2',
                                    loss='squared_hinge'))])

#Train Data
model.fit(x_train, y_train)
pred = model.predict(x_test)
print("training", accuracy_score(y_test, pred))

#Test Data
X = []
for i in range(testdf.shape[0]):
    X.append(clean_str(testdf.iloc[i][0]))
Y = np.array(testdf["catclass"])
Y = np.char.mod('%d', Y)

pred2 = model.predict(X)
newtestdf = pd.concat([testdf, pd.DataFrame(pred2)], axis=1)
newtestdf.columns = ['Comment','Actual','Predicted']
print("testing", accuracy_score(Y, pred2))


filename = 'mdl.sav'
pickle.dump(model, open(filename, 'wb'))