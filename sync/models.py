from dataclasses import dataclass
from typing import List, NamedTuple, Dict

import pandas as pd


@dataclass
class Task:
    uuid: str
    spreadsheet_id: str
    target: str
    columns: List[str]
    keys: List[str] | None
    column_name_map: Dict[str, str] | None
    column_dtype_map: Dict[str, str] | None


class DataSet(NamedTuple):
    name: str
    dataframe: pd.DataFrame

    def __eq__(self, other):
        if isinstance(other, DataSet):
            return self.name == other.name and self.dataframe.equals(other.dataframe)
        return False


class Sheet(NamedTuple):
    title: str
    data: List[list]
