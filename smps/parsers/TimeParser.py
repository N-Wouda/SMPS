import logging
import warnings
from collections import namedtuple
from typing import List

from smps.classes import DataLine
from .Parser import Parser

StageOffset = namedtuple("StageOffset", "var constr period")
logger = logging.getLogger(__name__)


class TimeParser(Parser):
    FILE_EXTENSIONS = [".tim", ".TIM", ".time", ".TIME"]
    STEPS = {
        "TIME": lambda self, data_line: self._process_time(data_line),
        "PERIODS": lambda self, data_line: self._process_periods(data_line),
    }

    def __init__(self, location):
        super().__init__(location)

        self._name: str = ""
        self._stage_offsets: List[StageOffset] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def stage_offsets(self) -> List[StageOffset]:
        return self._stage_offsets

    def _process_time(self, data_line: DataLine):
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
