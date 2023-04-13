import unittest
import random
import pandas
from mock import patch

from fitfile.data_rules.age_band_rule import (
    AgeBandRule,
)
from .test_abstract_data_rule import DataRuleTester

possible_outcomes = ['90+'] + [
    '{x} - {y}'.format(
        x=num * 10,
        y=(num + 1) * 10,
    ) for num in range(0, 9)
]


class AgeBandRuleTest(DataRuleTester, unittest.TestCase):
    def setUp(self):
        self.empty_dataframe = pandas.DataFrame()
        self.data_rule = AgeBandRule(fields=[])

    def test_when_empty_dataframe_returns_empty_dataframe(self):
        self.assertTrue(self.data_rule.apply_rule(self.empty_dataframe).empty)

    def test_when_no_fields_are_passed_no_transformation_occurs(self):
        dataframe = pandas.DataFrame([{'test_col': 23}])
        another_data_rule = AgeBandRule(fields=[])
        self.assertTrue(another_data_rule.apply_rule(dataframe).equals(dataframe))

    def test_can_pass_integer_ages(self):
        age_band_rule = AgeBandRule(fields=['age'])
        dataframe = pandas.DataFrame([{'age': 23}])
        self.assertEqual(age_band_rule.apply_rule(dataframe)['age'][0], '20 - 30')

    def test_randomized_integer_age_bands(self):
        age_band_rule = AgeBandRule(fields=['age'])
        dataframe = pandas.DataFrame([{'age': random.randint(0, 100)} for i in range(0, 10000)])
        [
            self.assertIn(age_transformed, possible_outcomes) for age_transformed in
            age_band_rule.apply_rule(dataframe)['age']
        ]

    def test_randomized_float_age_bands(self):
        dataframe = pandas.DataFrame([{'age': random.uniform(0, 100)} for i in range(0, 10000)])
        age_band_rule = AgeBandRule(fields=['age'])
        [
            self.assertIn(age_transformed, possible_outcomes) for age_transformed in
            age_band_rule.apply_rule(dataframe)['age']
        ]

    def test_accepts_iso_formatted_dates(self):
        dataframe = pandas.DataFrame(
            [{'dob': '2010-10-05'}]
        )
        age_band_rule = AgeBandRule(fields=['dob'])
        [
            self.assertIn(age_transformed, possible_outcomes) for age_transformed in
            age_band_rule.apply_rule(dataframe)['dob']
        ]

    # When dates are wrong

    def test_calls_on_validation_error_and_returns_original_value_on_wrong_iso_format(self):
        dataframe = pandas.DataFrame(
            [{'dob': '2010-23-05'}]
        )
        age_band_rule = AgeBandRule(fields=['dob'])
        with patch.object(age_band_rule, 'on_validation_error') as mock_on_validation_error:
            results = age_band_rule.apply_rule(dataframe)
        mock_on_validation_error.assert_called()
        self.assertEqual(results['dob'][0], '2010-23-05')

    def test_calls_on_validation_error_and_returns_original_value_on_negative_age(self):
        dataframe = pandas.DataFrame([{'age': -23}])
        negative_age = AgeBandRule(fields=['age'])
        with patch.object(negative_age, 'on_validation_error') as mock_on_validation_error:
            results = negative_age.apply_rule(dataframe)
        mock_on_validation_error.assert_called()
        self.assertEqual(results['age'][0], '-23')

    def test_calls_on_validation_error_when_dob_is_on_the_future(self):
        dataframe = pandas.DataFrame([{'dob': '2024-12-12'}])
        negative_age = AgeBandRule(fields=['dob'])
        with patch.object(negative_age, 'on_validation_error') as mock_on_validation_error:
            results = negative_age.apply_rule(dataframe)
        mock_on_validation_error.assert_called()
        self.assertEqual(results['dob'][0], '2024-12-12')
