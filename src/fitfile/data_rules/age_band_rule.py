import datetime

from dateutil.relativedelta import relativedelta
from typing import Union
from fitfile.data_rules.abstract_data_rule import AbstractDataRule
from .exceptions import AgeDatumException


class AgeBandRule(AbstractDataRule):
    def __repr__(self) -> str:
        return 'Rule one – Age Band Group 0-10, 10-20 ... 90+'

    def transform_datum(self, datum: Union[str, int, float]) -> str:
        """
        Transforms a single datapoint, onto an age band of 10 up to 90+
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        if isinstance(datum, int) or isinstance(datum, float):
            return self._to_ten_up_to_ninety_multiple(int(datum))
        date_of_birth = datetime.date.fromisoformat(datum)
        now = datetime.datetime.now()
        return self._to_ten_up_to_ninety_multiple(relativedelta(now, date_of_birth).years)

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

    def validate_datum(self, datum: Union[str, int, float]) -> None:
        """
        Validates a dob/age datum depending on type
        :param datum: The datapoint to validate
        :return: None, raises AgeDatumException
        """
        if isinstance(datum, int) or isinstance(datum, float):
            return self._validate_numerical_age(datum)
        return self._validate_isoformat_date(datum)

    @staticmethod
    def _validate_numerical_age(datum: Union[int, float]) -> None:
        """
        Validates an age with a numerical value
        :param datum: The datapoint to validate, either an int or a float
        :return: None
        """
        if datum < 0:
            raise AgeDatumException(
                'Negative values are not supported for age, got {}'.format(datum))

    @staticmethod
    def _validate_isoformat_date(datum: str) -> None:
        """
        Validates an iso format date datapoint
        :param datum: The datapoint to validate
        :return: None
        """
        try:
            now = datetime.datetime.now()
            date_of_birth = datetime.datetime.fromisoformat(datum)
            if date_of_birth > now:
                raise AgeDatumException('Date of birth is in the future, {}'.format(date_of_birth))
        except ValueError as e:
            raise AgeDatumException(e)
