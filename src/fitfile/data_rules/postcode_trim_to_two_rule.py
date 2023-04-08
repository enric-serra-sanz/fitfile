import pandas
from typing import Union
from fitfile.data_rules.abstract_data_rule import AbstractDataRule
from .exceptions import PostCodeValidationException
from copy import deepcopy


class PostCodeTrimToTwoRule(AbstractDataRule):
    def __repr__(self) -> str:
        return 'Rule one – Age Band Group'

    def apply_rule(self) -> pandas.DataFrame:
        """
        Overwrites the original apply_rule, and does a group by and conditional before transforming
        :return: A transformed dataframe
        """
        new_df = deepcopy(self.dataframe)
        for field in self.fields:
            # Count how many times this postcode is seen, and use it as a where clause to transform
            # or not
            new_df = new_df.groupby(field).size().reset_index(  # type: ignore
                name='postcode_counts')
            new_df[field] = new_df[field].where(new_df['postcode_counts'] < 10).apply(
                self.transform_datum
            )
        new_df.drop('postcode_counts')
        return new_df

    def transform_datum(self, datum: str) -> str:
        """
        Transforms a single datapoint, onto an age band of 10 up to 90+
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        try:
            # TODO: This entire method should be in abstract class
            self.validate_postcode(datum)
            return datum[0:2]
        except Exception as e:
            self.on_validation_error(datum, e)
            return datum

    def on_validation_error(self, datum: Union[str, int, float], exception: Exception) -> None:
        """
        What to do when a validation fails
        :param datum:
        :param exception:
        :return:
        """
        pass

    @staticmethod
    def validate_postcode(to_validate: str) -> None:
        """
        Validates a postcode string
        :param to_validate:
        :return:
        """
        # Not going to properly validate as I would go insane checking the rules, just going to
        # Check it is a str, and raise Exception is length too short or too long
        if not isinstance(to_validate, str):
            raise PostCodeValidationException('Postcode is not a str, instead got {} on {}'.format(
                type(to_validate), to_validate
            ))

        if len(to_validate) > 3:
            raise PostCodeValidationException(
                'Postcode is supposed to be length 6-9, got {}'.format(to_validate))
