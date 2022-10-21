from enum import Enum
from typing import List

import ipdb
import lightgbm as lgb
import numpy as np
import optuna
from config import logger
from models.src.classesdata import HyperParameterDirection, ProblemTypes, EvalFunctions
from models.src.helpers.dataloader import Data
from models.src.helpers.parameters import HyperParameters


class LightGBMTrainer():
    """
    Test
    """

    def __init__(self, data: Data, problemType: Enum):
        self.data = data
        self.problemType = problemType

    def convert_to_lgb(self):
        self.dtrain = lgb.Dataset(self.data.X_train, label=self.data.y_train)
        self.dvalid = lgb.Dataset(self.data.X_test, label=self.data.y_test)

    def preprocess_data(self) -> None:
        logger.info("Preprocessing Data")
        logger.info(self.data.traindf.head(10))
        logger.info("Done Preprocessing Data")

    def train(self, params: dict, eval_rounds: int, stopping_rounds: int) -> lgb.LGBMModel:

        # Creating Call Backs
        log_eval = lgb.log_evaluation(period=eval_rounds)
        early_stopping = lgb.early_stopping(stopping_rounds=stopping_rounds)

        # Applying Hyperparemeters/Callbacks and Running Training
        model = lgb.train(params, self.dtrain, valid_sets=[
                          self.dvalid], callbacks=[log_eval, early_stopping])

        return model

    def hyperparametertune(self, eval_rounds: int, stopping_rounds: int, total_trials: int, direction: HyperParameterDirection) -> optuna.trial.FrozenTrial:
        """
        This Methods runs the hyperparemeter search for your algo:

        Args:
            eval_rounds: Number of rounds bore verbose prints
            stopping_roungs: then number of epoch training runs for where there is no improvemnt in evaluation metric

        """
        def objective(trial: optuna.Trial) -> float:

            # Getting The Respective Hyperparemeters
            param = HyperParameters(self.problemType, trial).lightgbm()
            param['n_estimators'] = 1000

            # Training models with params
            mdl = self.train(param, eval_rounds, stopping_rounds)

            # Running Predictipns
            preds = mdl.predict(self.data.X_test)
            if self.problemType == ProblemTypes.BINARY:
                preds = np.rint(preds)

            eval_func = EvalFunctions.get_eval_func(self.problemType)
            metric = eval_func(self.data.y_test, preds)

            return metric

        # Running The HyperParameter Search
        study = optuna.create_study(pruner=optuna.pruners.MedianPruner(
            n_warmup_steps=10), direction=direction.value)
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        study.optimize(objective, n_trials=total_trials)
        trial = study.best_trial

        # Logging The Trial
        self.log_trial(study)

        return trial

    def log_trial(self, study: optuna.Study):
        """
        This Functions Print the Paramaters of the best model
        Args:
            study: The optuna study
            trial: The 
        """
        logger.info("Number of finished trials: {}".format(len(study.trials)))
        logger.info("Best trial:")
        logger.info(f"  Value: {study.best_trial.value}")
        logger.info("  Params: ")
        for key, value in study.best_trial.params.items():
            logger.info(f"    {key}: {value}")

    def predict(self, model: lgb.LGBMModel) -> List[float]:
        predictions = model.predict(self.data.X_test)
        return predictions

    def default_train(self) -> lgb.LGBMModel:

        params = {'objective': self.problemType.value}

        model = lgb.train(params=params, train_set=self.dtrain,
                          valid_sets=[self.dvalid])
        preds = model.predict(self.data.X_test)

        if self.problemType == ProblemTypes.BINARY:
            preds = np.rint(preds)

        eval_func = EvalFunctions.get_eval_func(self.problemType)
        metric = eval_func(self.data.y_test, preds)

        print(f'Metric: {metric}')

        return model
