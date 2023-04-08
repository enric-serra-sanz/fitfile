from abc import (
    ABC,
    abstractmethod,
)
import pandas
from typing import Any


class AbstractDataRule(ABC):
    def __init__(self, dataframe: pandas.DataFrame, field_list: list[str] = None) -> None:
        self.dataframe: pandas.DataFrame = dataframe
        self.field_list: list[str] = field_list

    @abstractmethod
    def apply_rule(self) -> pandas.DataFrame:
        """
        Apply this specific rule to the dataframe and return a transformed dataframe
        :return: A pandas.DataFrame with the specific transformation applied
        """
        pass

    @abstractmethod
    def transform_datum(self, datum: Any) -> Any:
        """
        Transforms a single datapoint
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        pass
