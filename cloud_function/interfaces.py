from typing import Protocol, runtime_checkable, Union, TypedDict

import pandas as pd


@runtime_checkable
class Model(Protocol):
    """Interface of Model object that will be used in AWS lambda function.

    :attr input_columns: list of column names that are used as input for the model.
    :method cloud_function: function that takes a dataframe and returns a series of predictions.
    """
    input_columns: list[str]

    def run_predict(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        ...


class PredictionRequestBody(TypedDict):
    # value as {column_name: [value1, value2, ...]}
    ColumnNames: list[str]
    Values: dict[str, list[Union[int, float]]]


class PredictionResponseBody(TypedDict):
    result: list[Union[int, float]]

