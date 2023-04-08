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


class AbstractDataRule(ABC):
    def __init__(self, dataframe: pandas.DataFrame, fields: Optional[List[str]] = None) -> None:
        self.dataframe: pandas.DataFrame = dataframe
        if fields is None:
            fields = []
        self.fields: List[str] = fields

    @abstractmethod
    def apply_rule(self) -> pandas.DataFrame:
        """
        Apply this specific rule to the dataframe and return a transformed dataframe, a no side
        effect function, performance notice the deepcopy, if performance is an issue then modify
        the original dataframe and live with side effects
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

    @abstractmethod
    def on_validation_error(self, datum: Any, exception: Exception) -> None:
        """
        What to do when an entry fails to validate (usually log it, stop or take other actions)
        :param datum: An entry
        :param exception: The Exception to raise
        :return: None
        """
        pass