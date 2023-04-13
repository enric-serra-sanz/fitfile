import unittest
import pandas
from mock import patch

from fitfile.data_rules.postcode_trim_to_three_rule import (
    PostCodeTrimToThreeRule,
)
from .test_abstract_data_rule import DataRuleTester
from faker import Faker


class PostCodeTrimToThreeTest(DataRuleTester, unittest.TestCase):
    def setUp(self):
        self.empty_dataframe = pandas.DataFrame()
        self.data_rule = PostCodeTrimToThreeRule(fields=[])

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
        another_data_rule = PostCodeTrimToThreeRule(fields=[])
        self.assertTrue(another_data_rule.apply_rule(dataframe).equals(dataframe))

    def test_can_parse_postcodes(self):
        dataframe = pandas.DataFrame(
            [{'postcode': 'OX15XJ'},
             {'postcode': 'NY13TY'}])
        postcode_rule = PostCodeTrimToThreeRule(fields=['postcode'])
        result_df = postcode_rule.apply_rule(dataframe)
        self.assertEqual(result_df['postcode'][0], 'OX1')
        self.assertEqual(result_df['postcode'][1], 'NY1')

    @staticmethod
    def test_fails_with_4_numbers_postcodes():
        dataframe = pandas.DataFrame([{'postcode': 'OX1555XJ'}])
        postcode_rule = PostCodeTrimToThreeRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            postcode_rule.apply_rule(dataframe)
        mock_on_validation_error.assert_called()

    @staticmethod
    def test_fails_with_wrong_starting_character_postcodes():
        dataframe = pandas.DataFrame([{'postcode': '15XJ'}])
        postcode_rule = PostCodeTrimToThreeRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            postcode_rule.apply_rule(dataframe)
        mock_on_validation_error.assert_called()

    @staticmethod
    def test_fails_with_no_number_postcodes():
        dataframe = pandas.DataFrame([{'postcode': 'OXDS'}])
        postcode_rule = PostCodeTrimToThreeRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            postcode_rule.apply_rule(dataframe)
        mock_on_validation_error.assert_called()

    def test_postcode_too_short_returns_same_postcode_but_calls_on_error(self):
        dataframe = pandas.DataFrame([{'postcode': 'O'}])
        postcode_rule = PostCodeTrimToThreeRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            results = postcode_rule.apply_rule(dataframe)
        mock_on_validation_error.assert_called()
        self.assertEqual(results['postcode'][0], dataframe['postcode'][0])

    def test_postcode_too_long_returns_same_postcode_but_calls_on_error(self):
        dataframe = pandas.DataFrame([{'postcode': 'OX1332 NYAAFDS44343'}])
        postcode_rule = PostCodeTrimToThreeRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            results = postcode_rule.apply_rule(dataframe)
        mock_on_validation_error.assert_called()
        self.assertEqual(results['postcode'][0], dataframe['postcode'][0])

    def test_should_parse_fake_postcodes_to_three_characters(self):
        dataframe = pandas.DataFrame(self.random_postcodes)
        postcode_rule = PostCodeTrimToThreeRule(fields=['postcode'])
        with patch.object(postcode_rule, 'on_validation_error') as mock_on_validation_error:
            results = postcode_rule.apply_rule(dataframe)
        self.assertFalse(mock_on_validation_error.called)
        self.assertTrue(all([len(x) == 3 for x in results['postcode']]))
