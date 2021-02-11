import logging
import warnings
from typing import List, Tuple

from smps.classes import DataLine
from .Parser import Parser

logger = logging.getLogger(__name__)


class TimeParser(Parser):

    def __init__(self, location):
        super().__init__(location)

        self._param = "IMPLICIT"
        self._stage_names: List[str] = []

        # For an IMPLICIT specification.
        self._stage_offsets: List[Tuple[str, str]] = []

        # For an EXPLICIT specification.
        self._explicit_constraints: List[Tuple[str, str]] = []
        self._explicit_variables: List[Tuple[str, str]] = []

    @property
    def _file_extensions(self):
        return [".tim", ".TIM", ".time", ".TIME"]

    @property
    def _steps(self):
        return {
            "TIME": self._process_time,
            "PERIODS": self._process_periods,
            "ROWS": self._process_rows,
            "COLUMNS": self._process_columns,
        }

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
        constraint to a stage.
        """
        return self._explicit_constraints

    @property
    def explicit_variables(self) -> List[Tuple[str, str]]:
        """
        Returns a list of (var, period)-tuples, that uniquely assigns each
        variable to a stage.
        """
        return self._explicit_variables

    @property
    def time_type(self) -> str:
        """
        Type of TIME file. Returns one of {"IMPLICIT", "EXPLICIT"}. In the
        former case, the CORE file is temporally ordered and can be parsed
        easily into different stages. In the latter, an explicit stage
        assignment is given for each row (constraint) and column (variable).
        """
        assert self._param in {"IMPLICIT", "EXPLICIT"}
        return self._param

    def _process_time(self, data_line: DataLine):
        if not data_line.has_second_header_word():
            msg = "Time file has no value for the TIME field."
            warnings.warn(msg)
            logger.warning(msg)
        else:
            self._name = data_line.second_header_word()

    def _process_periods(self, data_line: DataLine):
        assert data_line.has_third_name()

        period = data_line.third_name()
        self._stage_names.append(period)

        if self._param == "IMPLICIT":
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

        if data_line.has_second_header_word():
            param = data_line.second_header_word().upper()
        else:
            param = ""  # not set

        # Default is implicit (see Gassmann on the PERIODS section). So  we need
        # to update in case the param in EXPLICIT, the only other option.
        if self._state == "PERIODS" and param == "EXPLICIT":
            self._param = "EXPLICIT"
            return True

        return res
