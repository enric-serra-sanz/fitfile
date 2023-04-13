import datetime
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
from dateutil.relativedelta import relativedelta


class AbstractDataManager(ABC):
    def __init__(self, input_file_path: str, output_file_path: str, request_id: str,
                 logger: Optional[Any] = None) -> None:
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.request_id = request_id
        self._dataframe: Optional[pandas.DataFrame] = None
        self._rules: List[Any] = []
        if logger is None:
            logging.basicConfig(
                datefmt='%H:%M:%S',
                level=logging.INFO
            )
            logger = logging.getLogger('fitfile.data_manager')
        self.logger = logger

    def __repr__(self) -> str:
        return '{} for request ID: {} with rules: {}, on file: {}'.format(
            self.__class__.__name__,
            self.request_id,
            [r for r in self.rules],
            self.input_file_path,
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
        start = datetime.datetime.now()
        self.logger.info('Executing: {}, start time: {} '.format(self, start))
        to_save_df = deepcopy(self.dataframe)
        for rule in self.rules:

            to_save_df = rule.apply_rule(to_save_df)
        self.save_to_json_out(to_save_df)
        wallclock = relativedelta(datetime.datetime.now(), start).microseconds
        self.logger.info('Completed {} with status {} in {} microseconds'.format(
            self,
            self.error_string,
            wallclock
        ))

    @property
    def error(self) -> bool:
        """
        Returns the error status, which is the product of the error status of rules
        :return: Boolean, whether any of the rules have failed or not
        """
        return any([rule.error for rule in self.rules])

    @property
    def error_string(self) -> str:
        """
        Returns the task status as a string
        :return: A string representing the task status
        """
        return {
            False: 'SUCCESS',
            True: 'FAIL'
        }[self.error]
