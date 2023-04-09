from abc import (
    ABC,
    abstractmethod,
)
import pandas
from typing import (
    Any,
    List,
    Optional,
)
from copy import deepcopy


class AbstractDataRule(ABC):
    def __init__(self, fields: Optional[List[str]] = None) -> None:
        if fields is None:
            fields = []
        self.fields: List[str] = fields

    def apply_rule(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        """
        Apply this specific rule to the dataframe and return a transformed dataframe, where all
        age, date of birth, and year of birth fields are converted to a band of 10 up to 90+
        :return: A pandas.DataFrame with the specific transformation applied
        """
        new_df = deepcopy(dataframe)
        for field in self.fields:
            new_df[field] = new_df[field].apply(self.transform_datum, True)
        return new_df

    @abstractmethod
    def transform_datum(self, datum: Any) -> Any:
        """
        Transforms a single datapoint
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        pass

    @abstractmethod
    def on_validation_error(self, datum: Any, exception: Exception) -> None:
        """
        What to do when an entry fails to validate (usually log it, stop or take other actions)
        :param datum: An entry
        :param exception: The Exception to raise
        :return: None
        """
        pass
