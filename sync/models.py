from typing import List, NamedTuple

import pandas as pd


class DataSet(NamedTuple):
    name: str
    dataframe: pd.DataFrame

    def __eq__(self, other):
        if isinstance(other, DataSet):
            return self.name == other.name and \
                self.dataframe.equals(other.dataframe)
        return False


class Sheet(NamedTuple):
    title: str
    data: List[list]
