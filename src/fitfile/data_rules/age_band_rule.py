import datetime
import pandas

from dateutil.relativedelta import relativedelta
from typing import Union
from fitfile.data_rules.abstract_data_rule import AbstractDataRule
from copy import deepcopy


class AgeDatumException(Exception):
    pass


class AgeBandRule(AbstractDataRule):
    def __repr__(self) -> str:
        return 'Rule one – Age Band Group'

    def apply_rule(self) -> pandas.DataFrame:
        """
        Apply this specific rule to the dataframe and return a transformed dataframe, where all
        age, date of birth, and year of birth fields are converted to a band of 10 up to 90+
        :return: A pandas.DataFrame with the specific transformation applied
        """
        new_df = deepcopy(self.dataframe)
        for field in self.fields:
            new_df[field] = new_df[field].apply(self.transform_datum, True)
        return new_df

    def transform_datum(self, datum: Union[str, int, float]) -> str:
        """
        Transforms a single datapoint, onto an age band of 10 up to 90+
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        try:
            if isinstance(datum, int) or isinstance(datum, float):
                if datum < 0:
                    raise AgeDatumException(
                        'Negative values are not supported for age, got {}'.format(
                            datum
                        ))
                return self._to_ten_up_to_ninety_multiple(int(datum))
            date_of_birth = datetime.date.fromisoformat(datum)
            now = datetime.datetime.now()
            return self._to_ten_up_to_ninety_multiple(relativedelta(now, date_of_birth).years)
        except Exception as e:
            self.on_validation_error(datum, e)
            return str(datum)

    @staticmethod
    def _to_ten_up_to_ninety_multiple(age: int) -> str:
        """
        Converts an integer age to a string of the form '10 - 20' ... '90+'
        :param age: An integer representing the age
        :return: A string
        """
        modulo = min(90, (age // 10) * 10)
        if modulo == 90:
            return '90+'
        return '{modulo} - {modulo_plus_ten}'.format(
            modulo=modulo,
            modulo_plus_ten=modulo + 10,
        )

    def on_validation_error(self, datum: Union[str, int, float], exception: Exception) -> None:
        """
        What to do when a validation fails
        :param datum:
        :param exception:
        :return:
        """
        pass
