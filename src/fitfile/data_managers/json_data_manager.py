import pandas

from fitfile.data_managers.abstract_data_manager import AbstractDataManager


class JsonDataManager(AbstractDataManager):
    """Class to manage process with an input coming from json"""
    def load_data(self) -> pandas.DataFrame:
        return pandas.read_json(self.input_file_path)  # type: ignore
