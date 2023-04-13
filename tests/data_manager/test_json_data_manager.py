import os
import unittest
from .test_abstract_data_manager import DataManagerTester
from fitfile.data_managers import JsonDataManager


class JsonDataManagerTester(DataManagerTester, unittest.TestCase):
    def setUp(self):
        self.data_manager = JsonDataManager(input_file_path=os.path.join(os.path.dirname(
            __file__
        ), '../../20230320_FITFILEPythonTest/PatientCohorts.json'),
            output_file_path='test.json',
            request_id='TESTID123'
        )
