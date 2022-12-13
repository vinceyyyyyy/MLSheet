from typing import TypedDict, Protocol, runtime_checkable
from functools import partial

import pandas as pd


@runtime_checkable
class Model(Protocol):
    """Interface of Model object that will be used in AWS lambda function.

    :attr input_columns: list of column names that are used as input for the model.
    :method predict: function that takes a dataframe and returns a series of predictions.
    """
    input_columns: list[str]

    def run_predict(self, data: pd.DataFrame) -> pd.DataFrame | pd.Series:
        ...


class PredictionRequestBody(TypedDict):
    # value as {column_name: [value1, value2, ...]}
    ColumnNames: list[str]
    Values: dict[str, list[int | float]]


class PredictionResponseBody(TypedDict):
    result: list[int | float]

def add_method(obj, func):
        """Bind a function and store it in an object"""
        setattr(obj, func.__name__, partial(func, obj))