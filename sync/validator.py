from typing import Set

from .config import Config
from .models import DataSet


class Validator:
    def __init__(self, config: Config, values: Set[tuple]):
        self.validation_fields = config.validate
        self.values = values

    def validate(self, dataset: DataSet) -> DataSet:
        title, df = dataset
        df["validate"] = list(
            df[self.validation_fields].itertuples(index=False, name=None)
        )
        df = df.where(df.validate.isin(self.values)).dropna(how="all")
        df = df.drop(columns=["validate"])
        return DataSet(title, df)
