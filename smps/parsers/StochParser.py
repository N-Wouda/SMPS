import logging
import warnings
from typing import List, Optional

from smps.classes import DataLine, Scenario
from .Parser import Parser

logger = logging.getLogger(__name__)

_LINEAR_TRANSFORMATIONS = {"LINTR", "LINTRAN"}
_DISTRIBUTIONS = {"DISCRETE", "UNIFORM", "NORMAL", "GAMMA", "BETA",
                  "LOGNORM", "MVNORMAL"}


class StochParser(Parser):
    _file_extensions = [".sto", ".STO", ".stoch", ".STOCH"]
    _steps = {
        "STOCH": lambda self, data_line: self._process_stoch(data_line),
        "INDEP": lambda self, data_line: self._process_indep(data_line),
        "BLOCKS": lambda self, data_line: self._process_blocks(data_line),
        "SCENARIOS": lambda self, data_line: self._process_scenarios(data_line),
        "NODES": lambda self, data_line: self._process_nodes(data_line),
        "DISTRIB": lambda self, data_line: self._process_distrib(data_line),
    }

    def __init__(self, location):
        super().__init__(location)

        self._param = ""
        self._scenario: Optional[Scenario] = None
        # TODO

    @property
    def scenarios(self) -> List[Scenario]:
        return Scenario.scenarios()

    def _process_stoch(self, data_line: DataLine):
        self._name = data_line.second_header_word()

        if not data_line.second_header_word():
            msg = "Stoch file has no value for the STOCH field."
            warnings.warn(msg)
            logger.warning(msg)

    def _process_indep(self, data_line: DataLine):
        pass  # TODO

    def _process_blocks(self, data_line: DataLine):
        pass  # TODO

    def _process_scenarios(self, data_line: DataLine):
        assert self._param == "DISCRETE"

        if data_line.indicator() == "SC":  # new scenario
            scen = Scenario(data_line.first_name(),
                            data_line.second_name(),
                            data_line.third_name(),
                            data_line.first_number())

            self._scenario = scen
            return

        var = data_line.first_name()
        constr = data_line.second_name()
        value = data_line.first_number()

        assert self._scenario is not None  # just to be sure
        self._scenario.add_modification(constr, var, value)

        if data_line.has_third_name() and data_line.has_second_number():
            constr = data_line.third_name()
            value = data_line.second_number()

            self._scenario.add_modification(constr, var, value)

    def _process_nodes(self, data_line: DataLine):
        pass  # TODO

    def _process_distrib(self, data_line: DataLine):
        pass  # TODO

    def _transition(self, data_line):
        res = super()._transition(data_line)
        param = data_line.second_header_word().upper()

        if self._state == "STOCH" or self._state == "ENDATA":
            return res

        if not param:
            self._param = "DISCRETE"

            msg = f"Stoch type not given for {self._state}; assuming DISCRETE."
            logger.warning(msg)
            warnings.warn(msg)
            return True

        if self._state == "SCENARIOS" and param != "DISCRETE":
            msg = "Cannot parse non-DISCRETE scenarios."
            logger.error(msg)
            raise ValueError(msg)

        # The BLOCK or INDEP data is generated from a 2-parameter distribution.
        if param in _DISTRIBUTIONS:
            self._param = param
            return res

        # Linear transformations. These are (AFAIK) only defined for BLOCKS.
        if self._state == "BLOCKS" and param in _LINEAR_TRANSFORMATIONS:
            self._param = param
            return res

        return res
