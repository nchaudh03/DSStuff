from utils.projParams import *
from utils.dataSetup import *
from utils.mdl_xgboost import xgbModel
import h2o
from pathlib import *
import json
import pandas as pd

home_path = str(Path('.'))
h2o.init(ip="localhost", port=54321)







#Getting Best model and it parameters
pth = f'{home_path}\models\mdl_stats.txt'
mdls_log = pd.read_csv(pth)
mdls_log['avg'] = (mdls_log.f0point5_pre + mdls_log.f0point5_rec)/2
mdls_log.sort_values(by = 'avg', ascending = False, inplace = True) 
f1, f0point5,name = (mdls_log.f1.values[0],mdls_log.f0point5.values[0],mdls_log.name.values[0])
mdlpth = f'/app/models/{name}.zip'


#Testing best model on test data
test_data = load_single_ord(home_path)
clf = xgbModel(train=None, test=test_data)
clf.load_model(path=mdlpth, f1=f1/100,f0point5=f0point5/100)

prd,_ = clf.predict()
print(mdls_log)
print(prd)
