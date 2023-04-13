import pandas
from fitfile.data_rules.abstract_data_rule import AbstractDataRule
from .exceptions import PostCodeValidationException
from copy import deepcopy


class PostCodeTrimToTwoRule(AbstractDataRule):
    def __repr__(self) -> str:
        return 'Rule three – Trim postcode to 2 when less than 10 entries'

    def apply_rule(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        """
        Overwrites the original apply_rule, and does a group by and conditional before transforming
        :return: A transformed dataframe
        """
        def transform_if_lt_ten(row):  # type: ignore
            """
            Inner function to keep context
            :param row: The row to process
            :return: Modified row if counts < 10, unmodified row otherwise
            """
            try:
                self.validate_datum(row[field])
            except Exception as e:
                self.on_validation_error(row, e)
                return row
            if row['postcode_counts'] < 10:
                row[field] = self.transform_datum(row[field])
            return row

        toreturn_dataframe = deepcopy(dataframe)
        for field in self.fields:

            toreturn_dataframe['postcode_counts'] = toreturn_dataframe.groupby(  # type: ignore
                field)[field].transform('count')
            toreturn_dataframe = pandas.DataFrame(
                toreturn_dataframe.apply(transform_if_lt_ten, axis=1))
        return toreturn_dataframe

    def transform_datum(self, datum: str) -> str:
        """
        Transforms a single datapoint, onto an age band of 10 up to 90+
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        return datum[0:2]

    def validate_datum(self, to_validate: str) -> None:
        """
        Validates a previously trimmed to length 3 postcode string
        :param to_validate:
        :return:
        """
        if not isinstance(to_validate, str):
            raise PostCodeValidationException('Postcode is not a str, instead got {} on {}'.format(
                type(to_validate), to_validate
            ))
        if len(to_validate) != 3:
            raise PostCodeValidationException(
                'Postcode is supposed to be length 3, got {}'.format(to_validate))
