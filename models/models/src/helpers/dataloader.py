from pathlib import Path
from xmlrpc.client import Boolean

import pandas as pd
from config import logger
from sklearn import datasets, model_selection

#Assumes we are using a CSV or Sample Data
class Data():
    """
    Assumes we are using a CSV or Sample Data. The data class for this project. The two required fields are sample_data
    and data_type. If sample_data is True you one need data_type if it False you need all fields.

    Args:
        sample_dta: If you dont have data setting this to true will create some sampel data for you
        data_type: The type of problem yuo are trying to solve
        path : location to csv
        features: list of features you want to use from csv
        target: the variable you want to predict
        single_file: Boolear to identity if you have just a train file on both train test
        split_data: if you have a single train file do you want to split it

    """
    def __init__(self,sample_data=True, data_type = "regression", path=Path('.'), features=None, target=None, single_file=None, split_data=None):
        self.path = path
        self.split_data = split_data
        self.feature_columns = features
        self.target_column = target
        self.single_file = single_file
        self.data_type = data_type

        # Runnning Read Data
        if sample_data:
            self.X_train, self.y_train, self.X_test, self.y_test = self.create_sample_data(
                data_type)
        else:
            self.X_train, self.y_train, self.X_test, self.y_test = self.read_data(
                path)

    def create_sample_data(self, data_type):
        if data_type == 'regression':
            data = datasets.make_regression(n_samples=1000, n_features=20, n_informative=15)
            X_train, X_test, y_train, y_test = model_selection.train_test_split(
                data[0], data[1], test_size=0.33, random_state=42
            )
            return X_train, y_train, X_test, y_test

        elif data_type == 'binary':
            data = datasets.make_classification(n_samples=1000, n_features=20, n_informative=15)
            X_train, X_test, y_train, y_test = model_selection.train_test_split(
                data[0], data[1], test_size=0.33, random_state=42
            )
            return X_train, y_train, X_test, y_test

        elif data_type == "multiclass":
            data = datasets.make_multilabel_classification()
            X_train, X_test, y_train, y_test = model_selection.train_test_split(
                data[0], data[1], test_size=0.33, random_state=42
            )
            return X_train, y_train, X_test, y_test

        else:
            print("Not supported Datatype: Raise Error")

    def read_data(self):
        if self.single_file:
            train_data = pd.read_csv(self.path / "train.csv`")

            #---Downsample----#
            #---Downsample----#

            X_train = train_data[self.feature_columns]
            y_train = train_data[self.target_column]

            if self.split_data:
                X_train, y_train, X_test, y_test = model_selection.train_test_split(
                    X_train, y_train, test_size=0.33, random_state=42
                )
            else:
                X_test = None
                y_test = None

        else:
            train_data = pd.read_csv(self.path / "train.csv`")
            test_data = pd.read_csv(self.path / "test.csv`")

            #---Downsample----#
            #---Downsample----#

            X_train = train_data[self.feature_columns]
            y_train = train_data[self.target_column]
            X_test = test_data[self.feature_columns]
            y_test = test_data[self.target_column]

        return X_train, y_train, X_test, y_test

    def downsample_data():
        pass

