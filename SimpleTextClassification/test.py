import os
import pandas as pd
import numpy as np
import pypyodbc
from warnings import filterwarnings
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, auc
import sys
filterwarnings('ignore')

from sklearn.svm import LinearSVC
from stringcleaner import clean_str
import pickle

#tstDate = sys.argv[1]
tstDate = '2020-08-01'
Newmdl = pickle.load(open("mdl.sav", "rb"))

testQuery = """ """.format(tstDate)  #test data

cnxn = pypyodbc.connect(r"Driver={driver};"
                        "Server=server;"
                        "Database=database;"
                        "Trusted_Connection=yes")


testdf = pd.read_sql(testQuery, cnxn)
		   
X = []
for i in range(testdf.shape[0]):
    X.append(clean_str(testdf.iloc[i][0]))
Y = np.array(testdf["catclass"])
Y = np.char.mod('%d', Y)

pred3 = Newmdl.predict(X)
newtestdf1 = pd.concat([testdf, pd.DataFrame(pred3)], axis=1)
newtestdf1.columns = ['Comment','Actual','Predicted']
print("test Accuracy", accuracy_score(Y, pred3))



