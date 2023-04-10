from fitfile.data_rules.abstract_data_rule import AbstractDataRule
from .exceptions import PostCodeValidationException
import postcodes_uk  # type: ignore


class PostCodeTrimToThreeRule(AbstractDataRule):
    def __repr__(self) -> str:
        return 'Rule two – Trim postcode to 3 characters'

    def transform_datum(self, datum: str) -> str:
        """
        Transforms a single datapoint, onto an age band of 10 up to 90+
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        try:
            self.validate_postcode(datum)
            return datum[0:3]

        except PostCodeValidationException as e:
            self.on_validation_error(datum, e)
            return datum

    @staticmethod
    def validate_postcode(to_validate: str) -> None:
        """
        Validates a postcode string
        :param to_validate:
        :return:
        """
        # Leave the validation to postcodes_uk package
        if not postcodes_uk.validate(to_validate):
            raise PostCodeValidationException(
                'Postcode is supposed to be length 5-9, got {}'.format(to_validate))
