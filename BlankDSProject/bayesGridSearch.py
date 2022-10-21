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


#Training Grid Search
clf = xgbModel(train=train_data, test=test_data)
mdlparams = clf.bayes_grid_search(bnds=bayes_bounds,
                                 init_mdls=10,
                                 tot_mdls=10)
prd,mdl_stats = clf.predict()
print(mdlparams)
print(mdl_stats)

save_model  = True
#Prints Best Parameters, set SV to true to save the grid search parameters
#print_bstParams(clf.bst_mdl.actual_params.items(),sv=save_model)
if save_model:
    save_path = ''.join([home_path,'\models\\'])
    save_name = ''
    clf.save_model(save_path,save_name,mdl_stats)