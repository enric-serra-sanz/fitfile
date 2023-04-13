import unittest
from unittest.mock import patch
import os

from fitfile.data_managers.abstract_data_manager import AbstractDataManager


class DataManagerTester(object):
    def test_should_have_a_load_data_method(self):
        self.assertTrue(hasattr(self.data_manager, 'load_data'))
        self.assertTrue(callable(getattr(self.data_manager, 'load_data')))

    def test_should_have_a_run_method(self):
        self.assertTrue(hasattr(self.data_manager, 'run'))
        self.assertTrue(callable(getattr(self.data_manager, 'run')))

    def test_should_have_a_set_rules_method(self):
        self.assertTrue(hasattr(self.data_manager, 'set_rules'))
        self.assertTrue(callable(getattr(self.data_manager, 'set_rules')))

    def test_should_have_a_save_to_json_method(self):
        self.assertTrue(hasattr(self.data_manager, 'save_to_json_out'))
        self.assertTrue(callable(getattr(self.data_manager, 'save_to_json_out')))

    def test_should_have_a_dataframe(self):
        self.assertTrue(hasattr(self.data_manager, 'dataframe'))

    def test_should_have_an_input_filepath(self):
        self.assertTrue(hasattr(self.data_manager, 'input_file_path'))

    def test_should_have_an_output_filepath(self):
        self.assertTrue(hasattr(self.data_manager, 'output_file_path'))

    def test_should_have_a_request_id(self):
        self.assertTrue(hasattr(self.data_manager, 'request_id'))

    def test_should_have_a_logger(self):
        self.assertTrue(hasattr(self.data_manager, 'logger'))


class AbstractDataRuleTester(DataManagerTester, unittest.TestCase):
    @patch.multiple(AbstractDataManager, __abstractmethods__=set())
    def setUp(self):
        self.data_manager = AbstractDataManager(input_file_path=os.path.join(os.path.dirname(
            __file__
        ), '../../20230320_FITFILEPythonTest/customer.csv'),
            output_file_path='test.json',
            request_id='TESTID123')
