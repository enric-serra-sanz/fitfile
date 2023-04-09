import pandas

from fitfile.data_managers.abstract_data_manager import AbstractDataManager


class ExcelDataManager(AbstractDataManager):
    """Class to manage process with an input coming from excel"""
    def load_data(self) -> pandas.DataFrame:
        return pandas.read_excel(self.input_file_path)  # type: ignore
