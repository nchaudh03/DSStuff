from enum import Enum
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, root_validator
from sklearn import metrics

class ProblemTypes(Enum):
    REGRESSION = 'regression'
    MULTICLASS = "multiclass"
    BINARY = "binary"


class TrainingParams(Enum):
    TRAIN_PARAMS = {
        ProblemTypes.REGRESSION: {'objective': ProblemTypes.REGRESSION.value, 'metric': 'mse'},
        ProblemTypes.MULTICLASS: {'objective': ProblemTypes.MULTICLASS.value, 'metric': 'auc'},
        ProblemTypes.BINARY: {
            'objective': ProblemTypes.BINARY.value, 'metric': 'binary_logloss'}
    }


class EvalFunctions():
    @staticmethod
    def get_eval_func(problemType: ProblemTypes):
        evals = {
            ProblemTypes.REGRESSION: metrics.mean_squared_error,
            ProblemTypes.BINARY: metrics.accuracy_score,
            ProblemTypes.MULTICLASS: metrics.auc

        }

        return evals.get(problemType)


class HyperParameterDirection(Enum):
    MINIMIZE = 'minimize'
    MAXIMIZE = "maximize"


class DataFields(BaseModel):
    sample_data: bool
    data_type: str
    path: Optional[Path]
    features: Optional[List[str]]
    target: Optional[List[str]]
    single_file: Optional[bool]
    split_data: Optional[bool]

    @root_validator
    def check_none_values(cls, values):
        sample_data = values.get('sample_data')
        if sample_data == False:
            fields = list(values.keys())
            for i in fields:
                if i not in ['sample_data', 'split_data']:
                    if values.get(i) == None:
                        raise ValueError(
                            "If sample data is false all other fields need to be filled in")
        return values

    @root_validator
    def check_split_data(cls, values):
        if values.get('single_file'):
            if not values.get('split_data'):
                raise ValueError("With single file need split_data ")
        return values
