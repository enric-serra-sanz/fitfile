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
import logging


logging.basicConfig()


class AbstractDataManager(ABC):
    def __init__(self, input_file_path: str, output_file_path: str, request_id: str,
                 logger: Optional[Any] = None) -> None:
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.request_id = request_id
        self._dataframe: Optional[pandas.DataFrame] = None
        self._rules: List[Any] = []
        if logger is None:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
        self.logger = logger

    def __repr__(self) -> str:
        return '{} for request ID: {} with rules: {}'.format(
            self.__class__.__name__,
            self.request_id,
            [r for r in self.rules]
        )

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

    def save_to_json_out(self, dataframe: Optional[pandas.DataFrame], *args: Any,
                         **kwargs: Any) -> None:
        """
        Saves a dataframe to the output_file_path in json format
        :param dataframe: The dataframe to save
        :param args: additional args for to_json
        :param kwargs: additional kwargs for to_json
        :return: None
        """
        print('calling logger info')
        self.logger.info('Saving {} results to {}'.format(self, self.output_file_path))
        if dataframe is None:
            dataframe = self.dataframe
        orient = kwargs.pop('orient', 'records')
        indent = kwargs.pop('indent', 4)
        dataframe.to_json(  # type: ignore
            self.output_file_path,
            orient=orient,
            indent=indent,
            *args,
            **kwargs

        )

    def run(self) -> None:
        """
        Runs the data management job, copies the dataframe, applies all the rules in order and
        saves to a json out
        :return: None
        """
        self.logger.info('Executing {} '.format(self))
        to_save_df = deepcopy(self.dataframe)
        for rule in self.rules:
            to_save_df = rule.apply_rule(to_save_df)
        self.save_to_json_out(to_save_df)
