from fitfile.data_rules.abstract_data_rule import AbstractDataRule
from .exceptions import PostCodeValidationException


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

        except Exception as e:
            self.on_validation_error(datum, e)
            return datum

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

        if len(to_validate) > 9 or len(to_validate) < 5:
            raise PostCodeValidationException(
                'Postcode is supposed to be length 5-9, got {}'.format(to_validate))
