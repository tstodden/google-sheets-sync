import pandas as pd

from sync.config import Config
from sync.models import DataSet
from sync.models import Sheet


class Converter:
    def __init__(self, config: Config):
        self.config = config

    def convert(self, sheet_list: list[Sheet]) -> list[DataSet]:
        return [self._convert(sheet) for sheet in sheet_list]

    def _convert(self, sheet: Sheet) -> DataSet:
        title, data = sheet
        header_list, *data = data

        if self.config.column_name_map:
            header_list = self._rename_header_list(header_list)

        # create DataFrame
        data = self._resize_first_row(data, header_list)
        df = pd.DataFrame(data, columns=header_list)

        # general cleanup
        df = self._empty_string_to_none(df)
        df = self._remove_duplicate_columns(df)

        if self.config.keys:
            df = self._remove_duplicate_keys(df)

        if self.config.column_dtype_map:
            df = self._convert_dtype_from_map(df)

        if self.config.custom_values:
            df = self._assign_custom_values(df)

        df = self._reorder_columns(df)
        # finally replace all NA values to None to become NULL
        df = self._all_na_to_none(df)
        return DataSet(name=title, dataframe=df)

    def _rename_header_list(self, header_list: list[str]) -> list[str]:
        name_map = self.config.column_name_map or {}
        for i, header in enumerate(header_list):
            header_list[i] = name_map[header] if header in name_map else header
        return header_list

    def _resize_first_row(
        self, data: list[list[str]], header_list: list[str]
    ) -> list[list[str]]:
        first_row = data[0] if len(data) > 0 else []
        while len(first_row) < len(header_list):
            first_row.append("")
        return data

    def _empty_string_to_none(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.applymap(lambda x: x if x else None)

    def _remove_duplicate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.loc[:, ~df.columns.duplicated()]
        return df

    def _remove_duplicate_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        key_list = self.config.keys or []
        df = df.dropna(subset=key_list)  # drop empty keys
        df = df.drop_duplicates(subset=key_list)
        return df

    def _convert_dtype_from_map(self, df: pd.DataFrame) -> pd.DataFrame:
        dtype_map = self.config.column_dtype_map or {}
        for col_name, dtype in dtype_map.items():
            col = df.get(col_name)
            if col is None:
                continue  # skip converstion if col doesn't exist
            df[col_name] = self._convert_column_dtype(col, dtype)
        return df

    def _convert_column_dtype(self, col: pd.Series, dtype: str) -> pd.Series:
        if dtype == "int":
            col = col.map(_try_convert_string_to_int)
        elif dtype == "float":
            col = col.map(_try_convert_string_to_float)
        elif dtype == "datetime":
            col = col.map(_try_convert_string_to_datetime)
        else:
            raise NotImplementedError(f"dtype {dtype} is not valid")
        return col

    def _assign_custom_values(self, df: pd.DataFrame) -> pd.DataFrame:
        custom_values = self.config.custom_values or {}
        return df.assign(**custom_values)

    def _reorder_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.reindex(columns=self.config.columns)

    def _all_na_to_none(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.astype(object).where(df.notnull(), None)


def _try_convert_string_to_float(string: str) -> float | None:
    clean_string = _clean_numeric_string(string)
    return float(clean_string) if clean_string else None


def _try_convert_string_to_int(string: str) -> int | None:
    flt = _try_convert_string_to_float(string)
    return int(flt) if flt else None


def _try_convert_string_to_datetime(string: str) -> str | None:
    string = pd.Timestamp(string, tz="UTC").isoformat()
    return string if string != "NaT" else None


def _clean_numeric_string(string: str) -> str:
    clean_string = ""
    string = string or ""
    for c in string:
        clean_string += c if c not in ["#", "$", ","] else ""
    return clean_string


def create_converter(config: Config) -> Converter:
    if not config.type:
        converter = Converter(config)
    else:
        raise NotImplementedError("{config.type} is not a valid type")
    return converter
