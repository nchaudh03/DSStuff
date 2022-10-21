

unit_tst = False

#------------------------------------------Model Information--------------------------------------------#
'''
If New columns are added, need to add them to cols, col_types,
cols is the columns after the drop, col+types follows cols
'''

target = 'targe col name'
cols = []
col_types = ['enum','numeric'] #<- Column Types

assert len(cols) == len(col_types), "The Lenght of the columns and column types must be the same"

predictors = [x for x in cols if x!= target]
drop = [0,12]  #<- -- Drop column indexes


#XGB Specifig Metrics for early stoping
tol =0.005
rounds = 10
met = 'logloss'
fld_asmt = 'Stratified'

#------------------------------------------Best Model Parameters for Train----------------------------------#
params =  {}


#-----------------------------------Random Grid Search Parameters----------------------------------------------#
grid_params = {'ntrees': [500], 'max_depth': [5,10,15,20],'min_rows' : [0.01,0.1,1.0,3,5,10,15,20], 'seed': [1234]
              ,'sample_rate': [0.6,0.8,1.0], 'col_sample_rate': [0.6,0.8,1.0],'col_sample_rate_per_tree' : [0.7,0.8,0.9,1.0]
              ,'reg_alpha' : [0.001, 0.01, 0.1, 1, 10, 100], 'reg_lambda' : [0.001,0.01,0.1,0.5,1],'learn_rate' : [0.5,0.1,0.05,0.01]

            }

if unit_tst==True:
    max_mdl = 3
    max_runtime = 60
else:
    max_mdl = 1000
    max_runtime = 25000
g_strat = {'strategy': "RandomDiscrete"
          ,'max_models': max_mdl
          ,'max_runtime_secs': max_runtime
          ,'stopping_metric': met
          ,'stopping_tolerance': tol
          ,'stopping_rounds': rounds
        }

#-------------------------------------------------Bayes Grid Search Parameters---------------------------
bayes_bounds = {
    'max_depth':(5,30),
    'ntrees': (499,500),
    'min_rows':(0.01,30),
    'learn_rate':(0.001, 0.1),
    'sample_rate':(0.6,1),
    'col_sample_rate':(0.6,1),
    'col_sample_rate_per_tree' : (0.7,1.0),
    'reg_alpha' :(0.001,100),
    'reg_lambda' : (0.001,1)

}

bayes_niter = 2
bayes_ints = ['max_depth','ntrees']
