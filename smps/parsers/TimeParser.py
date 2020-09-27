import logging
import warnings
from collections import namedtuple
from typing import List

from smps.classes import DataLine
from .Parser import Parser

StageOffset = namedtuple("StageOffset", "variable constraint period")
logger = logging.getLogger(__name__)


class TimeParser(Parser):
    _FILE_EXTENSIONS = [".tim", ".TIM", ".time", ".TIME"]
    _STEPS = {
        "TIME": lambda self, data_line: self._process_time(data_line),
        "PERIODS": lambda self, data_line: self._process_periods(data_line),
    }

    def __init__(self, location):
        super().__init__(location)
        self._stage_offsets: List[StageOffset] = []

    @property
    def num_stages(self) -> int:
        """
        Number of stages in the problem.
        """
        return len(self._stage_offsets)

    @property
    def stage_names(self) -> List[str]:
        """
        Returns a list of stage names, that is, the names of each time period.
        """
        return [offset.period for offset in self._stage_offsets]

    @property
    def stage_offsets(self) -> List[StageOffset]:
        """
        Returns a list of StageOffset objects, which are named tuples with
        variable, constraint, and period attributes.
        """
        return self._stage_offsets

    def _process_time(self, data_line: DataLine):
        assert data_line.header() == "TIME"

        if len(data_line) > 15:
            self._name = data_line.first_data_name()
        else:
            warnings.warn("Time file has no value for the TIME field.")
            logger.warning("Time file has no value for the TIME field.")

    def _process_periods(self, data_line: DataLine):
        # TODO what about IMPLICIT/EXPLICIT?
        assert data_line.has_second_data_entry()

        var = data_line.name()
        constr = data_line.first_data_name()
        period = data_line.second_data_name()

        self._stage_offsets.append(StageOffset(var, constr, period))
