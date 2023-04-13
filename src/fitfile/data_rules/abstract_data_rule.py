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
    def __init__(self, fields: Optional[List[str]] = None, logger: Optional[Any] = None) -> None:
        if fields is None:
            fields = []
        self.fields: List[str] = fields
        self.logger = logger
        self.error: bool = False

    def apply_rule(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        """
        Apply this specific rule to the dataframe and return a transformed dataframe, where all
        age, date of birth, and year of birth fields are converted to a band of 10 up to 90+
        :return: A pandas.DataFrame with the specific transformation applied
        """
        new_df = deepcopy(dataframe)
        for field in self.fields:
            new_df[field] = new_df[field].apply(self.validate_and_transform, True)
        return new_df

    @abstractmethod
    def transform_datum(self, datum: Any) -> Any:
        """
        Transforms a single datapoint
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        pass

    def validate_and_transform(self, datum: Any) -> Any:
        try:
            self.validate_datum(datum)
            return self.transform_datum(datum)
        except Exception as e:
            self.on_validation_error(datum, e)
            return str(datum)

    def on_validation_error(self, datum: Any, exception: Exception) -> None:
        """
        What to do when an entry fails to validate (usually log it, stop or take other actions),
        default behaviour is to keep on processing as this might be a stream of data, overwrite on
        subclass to change behaviour.
        :param datum: An entry
        :param exception: The Exception to raise
        :return: None
        """
        if self.logger is not None:
            self.logger.error('Failed to validate {}, exception {}'.format(datum, exception))
        self.error = True

    @abstractmethod
    def validate_datum(self, datum):
        """
        Method to validate a data entry
        :return:
        """
        pass
