from enum import Enum
import uuid
from dataclasses import dataclass
from typing import NamedTuple

import pandas as pd


class DataType(str, Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    DATETIME = "datetime"

    @classmethod
    def from_string(cls, string: str) -> "DataType":
        match string:
            case "string":
                dtype = DataType.STRING
            case "int":
                dtype = DataType.INT
            case "float":
                dtype = DataType.FLOAT
            case "datetime":
                dtype = DataType.DATETIME
            case _:
                raise ValueError(f"{string} is not a valid datatype")
        return dtype


@dataclass
class Task:
    uuid: str
    spreadsheet_id: str
    table: str
    column_def: dict[str, DataType]
    schema: str | None
    key_list: list[str] | None
    column_rename_map: dict[str, str] | None

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, new_value):
        self.__dict__[key] = new_value

    @classmethod
    def from_dict(cls, dict_):
        return cls(
            uuid=str(uuid.uuid4()),
            spreadsheet_id=dict_["spreadsheet_id"],
            table=dict_["table"],
            column_def=_create_column_def(dict_["column_def"]),
            schema=dict_.get("schema"),
            key_list=dict_.get("key_list"),
            column_rename_map=dict_.get("column_rename_map"),
        )


def _create_column_def(column_def: dict[str, str]) -> dict[str, DataType]:
    new_column_def: dict[str, DataType] = dict()
    for col, dtype in column_def.items():
        new_column_def[col] = DataType.from_string(dtype)
    return new_column_def


class DataSet(NamedTuple):
    name: str
    dataframe: pd.DataFrame

    def __eq__(self, other):
        if isinstance(other, DataSet):
            return self.name == other.name and self.dataframe.equals(other.dataframe)
        return False

    def __repr__(self) -> str:
        return f"DataSet<name={self.name}, dataframe={self.dataframe}>"


class Sheet(NamedTuple):
    title: str
    data: list[list[str]]

    def __repr__(self) -> str:
        return f"Sheet<title={self.title}, data={self.data}>"
