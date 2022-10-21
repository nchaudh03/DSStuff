import optuna
from enum import Enum
from models.src.classesdata import TrainingParams

class HyperParameters():
    def __init__(self, problemType: Enum, trial: optuna.Trial):
        self.problemType = problemType
        self.trial = trial

    #The dict should hve enums
    def lightgbm(self) -> dict:

        train_param = TrainingParams.TRAIN_PARAMS.value

        generic = {
            'verbosity': self.trial.suggest_categorical('verbosity', [-1]),
            'boosting_type': self.trial.suggest_categorical('gbdt', ['gbdt']),
            'lambda_l1': self.trial.suggest_float('lambda_l1', 1e-8, 10.0, log=True),
            'lambda_l2': self.trial.suggest_float('lambda_l2', 1e-8, 10.0, log=True),
            'num_leaves': self.trial.suggest_int('num_leaves', 2, 256),
            'feature_fraction': self.trial.suggest_float('feature_fraction', 0.4, 1.0),
            'bagging_fraction': self.trial.suggest_float('bagging_fraction', 0.4, 1.0),
            'bagging_freq': self.trial.suggest_int('bagging_freq', 1, 7),
            'min_data_in_leaf': self.trial.suggest_int('min_data_in_leaf', 100, 4000),
            'max_depth': self.trial.suggest_int('max_depth', 3, 30),
            'learning_rate': self.trial.suggest_float('learning_rate', 0.001, 0.1),
            'feature_pre_filter': False,
            'objective': self.trial.suggest_categorical('objective', [train_param[self.problemType]['objective']]),
            'metric': self.trial.suggest_categorical('metric', [train_param[self.problemType]['metric']])
        }

        return generic

    def xgboost(self):

        binary = {
            'silent': 1,
            'objective': 'binary:logistic',
            'booster': self.trial.suggest_categorical('booster', ['gbtree', 'gblinear', 'dart']),
            'lambda': self.trial.suggest_float('lambda', 1e-8, 1.0, log=True),
            'alpha': self.trial.suggest_float('alpha', 1e-8, 1.0, log=True)
        }


def main():
    h = HyperParameters('test', 'binary')
    params = h.lightgbm()
    print(params)


if __name__ == "__main__":
    main()
