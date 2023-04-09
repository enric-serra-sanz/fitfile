import pandas

from fitfile.data_managers.abstract_data_manager import AbstractDataManager


class CsvDataManager(AbstractDataManager):
    """Class to manage process with an input coming from csv"""
    def load_data(self) -> pandas.DataFrame:
        return pandas.read_csv(self.input_file_path)
