import logging
import warnings
from typing import List, Tuple

from smps.classes import DataLine
from .Parser import Parser

logger = logging.getLogger(__name__)


class TimeParser(Parser):
    _file_extensions = [".tim", ".TIM", ".time", ".TIME"]
    _steps = {
        "TIME": lambda self, data_line: self._process_time(data_line),
        "PERIODS": lambda self, data_line: self._process_periods(data_line),
        "ROWS": lambda self, data_line: self._process_rows(data_line),
        "COLUMNS": lambda self, data_line: self._process_columns(data_line),
    }

    def __init__(self, location):
        super().__init__(location)

        self._time_type = "IMPLICIT"
        self._stage_names: List[str] = []

        # For an IMPLICIT specification.
        self._stage_offsets: List[Tuple[str, str]] = []

        # For an EXPLICIT specification.
        self._explicit_constraints: List[Tuple[str, str]] = []
        self._explicit_variables: List[Tuple[str, str]] = []

    @property
    def num_stages(self) -> int:
        """
        Number of stages in the problem.
        """
        return len(self._stage_names)

    @property
    def stage_names(self) -> List[str]:
        """
        Returns a list of stage names, that is, the names of each time period.
        """
        return self._stage_names

    @property
    def implicit_offsets(self) -> List[Tuple[str, str]]:
        """
        Returns a list of (var, constr)-tuples. These are implicit, in the sense
        that they delineate the start of a period, and assume the CORE file is
        ordered such that all (var, constr) pairs in between two offsets belong
        to that period.
        """
        return self._stage_offsets

    @property
    def explicit_constraints(self) -> List[Tuple[str, str]]:
        """
        Returns a list of (constr, period)-tuples, that uniquely assigns each
        constraint to a stage. Cached after first call.
        """
        return self._explicit_constraints

    @property
    def explicit_variables(self) -> List[Tuple[str, str]]:
        """
        Returns a list of (var, period)-tuples, that uniquely assigns each
        variable to a stage. Cached after first call.
        """
        return self._explicit_variables

    @property
    def time_type(self) -> str:
        assert self._time_type in {"IMPLICIT", "EXPLICIT"}
        return self._time_type

    def _process_time(self, data_line: DataLine):
        self._name = data_line.second_header_word()

        if not data_line.second_header_word():
            msg = "Time file has no value for the TIME field."
            warnings.warn(msg)
            logger.warning(msg)

    def _process_periods(self, data_line: DataLine):
        assert data_line.has_third_name()

        period = data_line.third_name()
        self._stage_names.append(period)

        if self._time_type == "IMPLICIT":
            # In the IMPLICIT formulation, the PERIODS section also contains
            # the (var, constr) offsets of this stage's CORE data.
            var = data_line.first_name()
            constr = data_line.second_name()

            self._stage_offsets.append((var, constr))

    def _process_rows(self, data_line: DataLine):
        constr = data_line.first_name()
        period = data_line.second_name()

        self._explicit_constraints.append((constr, period))

    def _process_columns(self, data_line: DataLine):
        var = data_line.first_name()
        period = data_line.second_name()

        self._explicit_variables.append((var, period))

    def _transition(self, data_line):
        res = super()._transition(data_line)
        param = data_line.second_header_word().upper()

        # Default is implicit (see Gassmann on the PERIODS section). So  we need
        # to update in case the param in EXPLICIT, the only other option.
        if self._state == "PERIODS" and param == "EXPLICIT":
            self._time_type = "EXPLICIT"
            return True

        return res
