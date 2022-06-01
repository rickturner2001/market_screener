from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, Any

from pandas import DataFrame

from classes.database.Database import Database
from classes.database.SP500Database import SP500Database


@dataclass
class DataframeConstructor(ABC):
    database: Union[Database, SP500Database]

    @abstractmethod
    def construct_df(self, *args: Any) -> DataFrame:
        pass
