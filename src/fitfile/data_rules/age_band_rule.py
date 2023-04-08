import pandas

from fitfile.data_rules.abstract_data_rule import AbstractDataRule


class AgeBandRule(AbstractDataRule):
    def __repr__(self):
        return 'Rule one – Age Band Group'

    def apply_rule(self) -> pandas.DataFrame:
        """
        Apply this specific rule to the dataframe and return a transformed dataframe, where all age, date of birth, and
        year of birth fields are converted to a band of 10 up to 90+
        :return: A pandas.DataFrame with the specific transformation applied
        """


    def transform_datum(self, datum: Any) -> Any:
        """
        Transforms a single datapoint
        :param datum: A single datapoint
        :return: A transformed datapoint
        """
        pass
