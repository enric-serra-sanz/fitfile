import unittest
import pandas
from mock import patch

from fitfile.data_rules.postcode_trim_to_two_rule import (
    PostCodeTrimToTwoRule,
)
from .test_abstract_data_rule import DataRuleTester
from faker import Faker
from copy import deepcopy


class PostCodeTrimToTwoTest(DataRuleTester, unittest.TestCase):
    def setUp(self):
        self.empty_dataframe = pandas.DataFrame()
        self.data_rule = PostCodeTrimToTwoRule(fields=[])
        # Faker generates fake postcodes, they are bound to the rules for postcodes, but there is
        # no guarantee they are real, would have to validate that
        fake = Faker('en_GB')
        Faker.seed(10)

        self.random_postcodes = [{'postcode': fake.postcode()} for _ in range(0, 50)]

    def test_when_empty_dataframe_returns_empty_dataframe(self):
        self.assertTrue(self.data_rule.apply_rule(self.empty_dataframe).equals(
            self.empty_dataframe))

    def test_when_no_fields_are_passed_no_transformation_occurs(self):
        dataframe = pandas.DataFrame([{'test_col': 23}])
        another_data_rule = PostCodeTrimToTwoRule(fields=[])
        self.assertTrue(another_data_rule.apply_rule(dataframe).equals(dataframe))

    def test_postcode_too_short_returns_same_postcode_but_calls_on_error(self):
        dataframe = pandas.DataFrame([{'postcode': 'O'}])
        postcode_rule = PostCodeTrimToTwoRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            results = postcode_rule.apply_rule(dataframe)
        mock_on_validation_error.assert_called()
        self.assertEqual(results['postcode'][0], dataframe['postcode'][0])

    def test_postcode_too_long_returns_same_postcode_but_calls_on_error(self):
        dataframe = pandas.DataFrame([{'postcode': 'OX1332 NYAAFDS44343'}])
        postcode_rule = PostCodeTrimToTwoRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            results = postcode_rule.apply_rule(dataframe)
        mock_on_validation_error.assert_called()
        self.assertEqual(results['postcode'][0], dataframe['postcode'][0])

    def test_validation_fails_if_rule_two_not_applied(self):
        dataframe = pandas.DataFrame(self.random_postcodes)
        postcode_rule = PostCodeTrimToTwoRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            postcode_rule.apply_rule(dataframe)
        self.assertTrue(mock_on_validation_error.called)

    def test_validation_fails_if_length_of_postcode_is_not_three(self):
        def test_of_length(length_to_evaluate):
            postcode = deepcopy(self.random_postcodes[0])
            postcode['postcode'] = postcode['postcode'][0:length_to_evaluate]
            dataframe = pandas.DataFrame([postcode])
            postcode_rule = PostCodeTrimToTwoRule(fields=['postcode'])
            with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
                postcode_rule.apply_rule(dataframe)
            self.assertTrue(mock_on_validation_error.called)
        for invalid_length in range(0, 3):
            test_of_length(invalid_length)
        for invalid_length in range(4, 20):
            test_of_length(invalid_length)

    def test_wont_trim_if_there_are_more_than_ten_entries_with_same_postcode(self):
        postcode = deepcopy(self.random_postcodes[0])
        postcode['postcode'] = postcode['postcode'][0:3]
        to_test = [postcode for _ in range(0, 20)]
        postcode_rule = PostCodeTrimToTwoRule(fields=['postcode'])
        results = postcode_rule.apply_rule(pandas.DataFrame(to_test))
        self.assertTrue(all([len(x) == 3 for x in results['postcode']]))
