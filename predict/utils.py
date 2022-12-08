from typing import TypedDict, Protocol, runtime_checkable

import pandas as pd

@runtime_checkable
class Model(Protocol):
    """Interface of Model object that will be used in AWS lambda function.

    :attr input_columns: list of column names that are used as input for the model.
    :method predict: function that takes a dataframe and returns a series of predictions.
    """
    input_columns: list[str]

    def predict(self, data: pd.DataFrame) -> pd.Series:
        ...



class PredictionRequestBody(TypedDict):
    # each value is a list of values for a row
    ColumnNames: list[str]
    Values: list[list[int | float]]


class PredictionResponseBody(TypedDict):
    result: list[int | float]
