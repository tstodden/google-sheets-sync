import logging
from typing import List, Tuple

import numpy as np
import pandas as pd

from .config import Config
from .models import DataSet
from .response import Sheet
from .validator import Validator

NUMERIC = ["float", "int"]


class Converter:
    def __init__(self, config: Config):
        self._config = config

    def set_validator(self, validator: Validator):
        self._validator = validator

    def convert(self, sheets: List[Sheet]) -> List[DataSet]:
        sets: List[DataSet] = []
        for sht in sheets:
            ds = self._convert_sheet_to_dataset(sht)
            ds, dups = self._clean_dataset(ds)
            if dups > 0:
                logging.warning(f"Removed {dups} duplicate(s) from {sht.title}")
            if self._config.validate:
                ds = self._validator.validate(ds)
            sets.append(ds)
        return sets

    def _clean_dataset(self, ds: DataSet) -> Tuple[DataSet, int]:
        ds = self._remove_duplicate_cols(ds)
        ds = self._rename_columns(ds)
        ds = self._assign_custom_values(ds)
        ds, dups = self._remove_duplicates(ds)
        ds = self._convert_dtypes(ds)
        ds = self._reorder_columns(ds)
        return ds, dups

    def _convert_sheet_to_dataset(self, sheet: Sheet) -> DataSet:
        df = pd.DataFrame(sheet.data, columns=sheet.data[0])
        df = df.drop(df.index[0]).reset_index(drop=True)
        return DataSet(name=sheet.title, dataframe=df)

    def _remove_duplicate_cols(self, dataset: DataSet) -> DataSet:
        title, df = dataset
        df = df.loc[:, ~df.columns.duplicated()]
        return DataSet(name=title, dataframe=df)

    def _rename_columns(self, dataset: DataSet) -> DataSet:
        title, df = dataset
        if self._config.column_name_map:
            df = df.rename(columns=self._config.column_name_map)
        return DataSet(name=title, dataframe=df)

    def _assign_custom_values(self, dataset: DataSet) -> DataSet:
        title, df = dataset
        if self._config.custom_values:
            df = df.assign(**self._config.custom_values)
        return DataSet(name=title, dataframe=df)

    def _convert_dtypes(self, dataset: DataSet) -> DataSet:
        title, df = dataset
        if self._config.column_dtype_map:
            df = self._cast_dataframe_from_dtype_map(df)
        return DataSet(name=title, dataframe=df)

    def _remove_duplicates(self, dataset: DataSet) -> Tuple[DataSet, int]:
        title, df = dataset
        dups = 0
        if self._config.keys:
            count = len(df.index)
            df = self._remove_empty_keys(df)
            df = df.drop_duplicates(subset=self._config.keys)
            dups = count - len(df.index)
        return DataSet(name=title, dataframe=df), dups

    def _reorder_columns(self, dataset: DataSet) -> DataSet:
        title, df = dataset
        df = df.replace(r"^\s*$", np.nan, regex=True)
        df = df.reindex(columns=self._config.columns)
        df = df.astype(object).where(df.notnull(), None)
        return DataSet(name=title, dataframe=df)

    def _remove_empty_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.replace("", np.nan)
        df = df.dropna(subset=self._config.keys)
        return df

    def _cast_dataframe_from_dtype_map(self, df: pd.DataFrame) -> pd.DataFrame:
        for col, dtype in self._config.column_dtype_map.items():
            if col in df.columns:
                df[col] = self._cast_column_to_dtype(df[col], dtype)
        return df

    def _cast_column_to_dtype(self, col: pd.Series, dtype: str) -> pd.Series:
        if dtype in NUMERIC:
            col = col.str.replace("$", "", regex=False)
            col = col.str.replace(",", "", regex=False)
            col = col.str.replace("#", "", regex=False)
            col = col.replace("", np.nan)
        col = col.astype(dtype)
        return col


def create_converter(config: Config) -> Converter:
    if not config.type:
        converter = Converter(config)
    else:
        raise NotImplementedError()
    return converter
