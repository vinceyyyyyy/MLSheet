from typing import Protocol, runtime_checkable, Union

import pandas as pd
import numpy as np


@runtime_checkable
class Model(Protocol):
    """Interface of Model object that will be used in AWS lambda function."""
    input_columns: list[str]  # list of column names that are used as input for the model

    def run_predict(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series, np.ndarray, list]:
        """function that takes a dataframe and returns a series of predictions"""
        ...
