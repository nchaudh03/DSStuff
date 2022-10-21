# BlankDSProject
Sample Directory to help kick start a project that loosely follows production guidelines.
This is designed using H20 as the backend. 

# Steps
* git clone https://github.com/nchaudh03/BlankDSProject
* Load full data into the data directory
  * Load small sample data into the data/unit_test directory
* Edit the utils/projectParams.py file with proper cols, col_types, and drops. 
* Run unit_test.py file to make sure everything flows. 
* Run the train.py to train the model on full data
* Run bayesGridSearch.py file to do hyper parameter search

# Completed algorithems
* XGBOOST Classifier - with f1 & f0point5 scores. 


# Things to add
* XGBOOST Regressor
* Auto feature Engineering
  * Featuretools
  * autofeat 
* NLP

