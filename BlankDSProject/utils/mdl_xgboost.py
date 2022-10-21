from utils.my_logger import *
from h2o.estimators import H2OXGBoostEstimator
from h2o.grid.grid_search import H2OGridSearch
from h2o import import_mojo
from utils.projParams import *
from csv import writer
from bayes_opt import BayesianOptimization
class xgbModel():
	@my_logger
	@my_timer
	def __init__(self, train,test):
		self.train = train
		self.test = test
		self.params = params
		self.predictors = predictors
		self.target = target
		self.bst_mdl = None
		self.stop_met = met
		self.stop_round=rounds
		self.stop_tol = tol
		self.fld_asmt = fld_asmt
	
	@my_logger
	@my_timer
	def fit(self):
		self.clf = H2OXGBoostEstimator(
						nfolds=5,
						seed=1234,
						stopping_metric= self.stop_met,
          			    stopping_tolerance= self.stop_tol,
          				stopping_rounds=self.stop_round,
						**self.params
						)
		self.clf.train(
			x=self.predictors,
			y=self.target,
			training_frame=self.train
		)
		self.train_perf = self.clf.model_performance(self.train)
		self.train_f1 = round(self.train_perf.find_threshold_by_max_metric('f1'),2)
		self.train_f0point5 = round(self.train_perf.find_threshold_by_max_metric('f0point5'),2)
		return (self.train_perf,self.train_f1, self.train_f0point5)
		
	@my_logger
	@my_timer		
	def predict(self):
		'''
		Will prioritize a grid search model if it avaliable
		'''
		if self.bst_mdl == None: 
			mdl_nm = self.clf.model_id
			self.test_perf =  self.clf.model_performance(self.test)
			prd = self.clf.predict(self.test)
			f1 = self.train_f1
			f0point5 = self.train_f0point5
		else: 
			mdl_nm = self.bst_mdl.model_id
			self.test_perf =  self.bst_mdl.model_performance(self.test)
			prd = self.bst_mdl.predict(self.test)
			f1 = self.grid_f1
			f0point5 = self.grid_f0point5

		mdl_stats = {
			'f1' : str(f1*100),
			'f0point5': str(f0point5*100),
			'f1_rec' : str(round(self.test_perf.recall(f1)[0][1],2)*100),
			'f1_pre' : str(round(self.test_perf.precision(f1)[0][1],2)*100),
			'f0point5_rec' : str(round(self.test_perf.recall(f0point5)[0][1],2)*100),
			'f0point5_pre' : str(round(self.test_perf.precision(f0point5)[0][1],2)*100),
			'unit_test' : str(unit_tst),
			'name' : mdl_nm

		}

		return prd,mdl_stats
	
	@my_logger
	@my_timer
	def grid_search(self, gridParams):
		self.grd_base =H2OXGBoostEstimator(
							nfolds=5
							,seed=1234
		                   ,stopping_metric = self.stop_met
                           ,stopping_tolerance= self.stop_tol
                           ,stopping_rounds = self.stop_round
                           ,fold_assignment =self.fld_asmt
                           ,keep_cross_validation_models =False
                           ,keep_cross_validation_predictions=False					
							)
		self.grd_clf = H2OGridSearch(
				   model=self.grd_base
				  ,search_criteria=g_strat
                  ,hyper_params=gridParams
                  )
		self.grd_clf.train(
					x=self.predictors,
					y=self.target,
					training_frame=self.train
			)
		self.lb = self.grd_clf.get_grid(
								sort_by=self.met
								,decreasing=True)
		self.bst_mdl = self.lb.models[0]
		self.grd_perf = self.bst_mdl.model_performance(self.train)
		self.grid_f1 = round(self.grd_perf.find_threshold_by_max_metric('f1'),2)
		self.grid_f0point5 = round(self.grd_perf.find_threshold_by_max_metric('f0point5'),2)
		#self.clf = self.bst_mdl
		return (self.grd_perf ,self.grid_f1, self.grid_f0point5)

	@my_logger
	@my_timer
	def bayes_grid_search(self, bnds,init_mdls=1, tot_mdls=1):
		def train_model(max_depth, 
            ntrees,
            min_rows, 
            learn_rate, 
            sample_rate, 
            col_sample_rate,
			col_sample_rate_per_tree,
			reg_alpha,
			reg_lambda
			):
			params = {
				'max_depth': int(max_depth),
				'ntrees': int(ntrees),
				'min_rows': int(min_rows),
				'learn_rate':learn_rate,
				'sample_rate':sample_rate,
				'col_sample_rate':col_sample_rate,
				'col_sample_rate_per_tree' : col_sample_rate_per_tree,
    			'reg_alpha' :reg_alpha,
    			'reg_lambda' : reg_lambda
			}
			model = H2OXGBoostEstimator(nfolds=5
			                           ,seed=1234
									  ,stopping_metric= self.stop_met
          							  ,stopping_tolerance= self.stop_tol
          							  ,stopping_rounds=self.stop_round
									 ,fold_assignment = self.fld_asmt
									   ,**params)
			model.train(x=self.predictors, y=self.target, training_frame=self.train)
			perf = model.model_performance(self.test)
			return perf.aucpr()

		optimizer = BayesianOptimization(
					f=train_model,
					pbounds=bnds,
					random_state=1,
				)
		optimizer.maximize(init_points=init_mdls, n_iter=tot_mdls)
		bst_params = optimizer.max['params']
		for key,val in bst_params.items():
			if key in bayes_ints:
				bst_params[key] = int(round(val))
		self.params = bst_params
		_,_,_ = self.fit()
		#self.bst_mdl = self.clf
		return optimizer.max

		
	
	def save_log(self,pth,sta):
		# Open file in append mode
		with open(pth, 'a+', newline='') as write_obj:
			# Create a writer object from csv module
			csv_writer = writer(write_obj)
			# Add contents of list as last row in the csv file
			csv_writer.writerow(sta.values())


	def save_model(self,path,name,mdl_stats):
		'''
		Will prioritize a grid search model if it avaliable
		'''
		if self.bst_mdl == None: mdl = self.clf
		else: mdl = self.bst_mdl
		fpath = ''.join([path,name])
		svpth = ''.join([path,'mdl_stats.txt'])
		self.save_log(svpth,mdl_stats)
		mdl.download_mojo(path=fpath,get_genmodel_jar=True)

		print(f"Save Done On Path {fpath}")


	def load_model(self,path,f1,f0point5):
		'''
		Load a Model and set it to clf
		'''
		self.clf=import_mojo(path)
		self.bst_mdl= None
		self.train_f1 = f1
		self.train_f0point5 = f0point5

		
		
		