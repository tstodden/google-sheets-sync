import abc
from typing import List

from sync.models import DataSet


class Connection(abc.ABC):
    @abc.abstractmethod
    def update(self, target: str, datasets: List[DataSet]):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_last_modified(self, name: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_last_modified(self, name: str, last_modified: str):
        raise NotImplementedError()
