from abc import (
    ABC,
    abstractmethod,
)
import pandas
from typing import (
    Any,
    List,
    Optional,
)
from copy import deepcopy
from fitfile.data_rules import AbstractDataRule


class AbstractDataManager(ABC):
    def __init__(self, input_file_path: str, output_file_path: str, process_id: str) -> None:
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.process_id = process_id
        self._dataframe: Optional[pandas.DataFrame] = None
        self._rules: List[Any] = []

    @property
    def dataframe(self) -> pandas.DataFrame:
        """
        Dataframe containing the data to be managed by this data manager
        :return:
        """
        if self._dataframe is None:
            self._dataframe = self.load_data()
        return self._dataframe

    def set_rules(self, rules: List[AbstractDataRule]) -> None:
        """
        Setter for rules to apply
        :param rules: A list of rules
        :return: None
        """
        self._rules = rules

    @property
    def rules(self) -> List[AbstractDataRule]:
        """
        The rules to apply (transformation/filtering for the dataframe)
        :return: A list
        """
        return self._rules

    @abstractmethod
    def load_data(self) -> pandas.DataFrame:
        pass

    def save_to_json_out(self, dataframe: Optional[pandas.DataFrame]) -> None:
        if dataframe is None:
            dataframe = self.dataframe
        dataframe.to_json(self.output_file_path, indent=4)  # type: ignore

    def run(self) -> None:
        to_save_df = deepcopy(self.dataframe)
        for rule in self.rules:
            to_save_df = rule.apply_rule(to_save_df)
        self.save_to_json_out(to_save_df)
