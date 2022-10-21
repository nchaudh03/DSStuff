from utils.projParams import *
from utils.dataSetup import *
from utils.mdl_xgboost import xgbModel
import h2o
from pathlib import *
import json
import pandas as pd

home_path = str(Path('.'))
h2o.init(ip="localhost", port=54321)


#Data Setup Module
train_data, test_data = download(home_path
                                ,testing=unit_tst
                                ) #Should do a assert test to make sure cols loaded properly
#train_data, test_data = [transform(x,y) for x,y in zip([train_data,test_data], ['train_data','test_data'])]



#Training Against Best Parameters
clf = xgbModel(train=train_data, test=test_data)
train_perf, train_f1, train_fopoint5 = clf.fit()
prd,mdl_stats = clf.predict()
print(mdl_stats)
print_bstParams(clf.clf.actual_params.items(),sv=False)
if True:
    save_path = ''.join([home_path,'\models\\'])
    save_name = ''
    clf.save_model(save_path,save_name,mdl_stats)