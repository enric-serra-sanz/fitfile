import unittest
from unittest.mock import patch

from fitfile.data_rules.abstract_data_rule import AbstractDataRule


class DataRuleTester(object):
    def test_should_have_an_apply_rule_method(self):
        self.assertTrue(hasattr(self.data_rule, 'apply_rule'))
        self.assertTrue(callable(getattr(self.data_rule, 'apply_rule')))

    def test_should_have_a_transform_datum_method(self):
        self.assertTrue(hasattr(self.data_rule, 'transform_datum'))
        self.assertTrue(callable(getattr(self.data_rule, 'transform_datum')))

    def test_should_have_an_on_validation_error_method(self):
        self.assertTrue(hasattr(self.data_rule, 'on_validation_error'))
        self.assertTrue(callable(getattr(self.data_rule, 'on_validation_error')))


class AbstractDataRuleTester(DataRuleTester, unittest.TestCase):
    @patch.multiple(AbstractDataRule, __abstractmethods__=set())
    def setUp(self):
        self.data_rule = AbstractDataRule()
