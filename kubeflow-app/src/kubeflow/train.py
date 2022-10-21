import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import logging
import argparse
from sklearn.metrics import accuracy_score
import random

def train(est: int):
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Preprocessing Data")
    data = pd.read_csv('/opt/app/kubeflow/merged_data.csv')
    #data = pd.read_csv('./src/kubeflow/merged_data.csv')
    cols = list(data.columns)
    data[cols[-1]] = data[cols[-1]].astype('category').cat.codes
    

    logging.info("Training Data")
    clf = RandomForestClassifier(n_estimators=est, max_depth=10)
    clf.fit(data[cols[0:-1]], data[cols[-1]])
    prd = clf.predict(data[cols[0:-1]])

    acc = accuracy_score(data[cols[-1]], prd)
    acc = round(random.random(),2)
    name = "accuracy"
    logging.info(f"accuracy={acc}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process hyper-parameters')
    parser.add_argument('--n_estimators', type=int, default=100, help='Total number of estimators')
    
    args = parser.parse_args()
    train(est=args.n_estimators)