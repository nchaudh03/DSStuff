import h2o
from utils.projParams import *
import json
def download(path,testing=False):
	h2o.remove_all()

	#Defining Path
	if testing == True: fpath = f'{path}/data/unit_test/'
	else: fpath = f'{path}/data/'
	
	#Getting Data
	train_data= h2o.upload_file( 
					 path=f'{fpath}train_datav2.txt'  
					,header=-1
					,destination_frame = 'train_data'
					,skipped_columns =drop
					,col_types = col_types
					,col_names = cols
					 )

	test_data = h2o.upload_file(
				     path=f'{fpath}test_datav2.txt'  
					,header=-1
					,destination_frame = 'test_data'
					,skipped_columns =drop
				    ,col_types = col_types
					,col_names = cols
                 )
	return(train_data, test_data)

def load_single_ord(path):
	fpath = path + '/data/'
	ord = h2o.upload_file(
				path=f'{fpath}tst_data.csv'  
				,header=-1
				,destination_frame = 'test_data'
				,skipped_columns =drop
				,col_types = col_types
				,col_names = cols
				)
	return ord

def transform(df,name):
	#Data transformation
	df = df.as_data_frame()
	#APPLY YOUR TRANSFORMS
	df = h2o.H2OFrame(df, destination_frame=name,column_types=col_types)
	return df


def print_bstParams(act,sv=True):
	f_params = {key:val for (key,val) in act if key in grid_params.keys()}
	name = 'z_bst_mdl_params.json'
	print(f'The best parameters are \n{f_params}')
	if sv==True:
		with open(f'{name}','w') as fp:
			json.dump(f_params,fp)
		print(f"Parameters saved to {name}")
