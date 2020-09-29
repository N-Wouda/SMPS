import logging
import warnings
from typing import List, Optional

from smps.classes import DataLine, Indep, Scenario
from .Parser import Parser

logger = logging.getLogger(__name__)

_LINEAR_TRANSFORMATIONS = {"LINTR", "LINTRAN"}
_MODIFICATIONS = {"ADD", "MULTIPLY", "REPLACE"}
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

        self._distribution = ""
        self._modification = ""

        self._scenario: Optional[Scenario] = None
        self._indep = Indep()
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
        self._indep.add_entry(self._distribution, data_line)

    def _process_blocks(self, data_line: DataLine):
        pass  # TODO

    def _process_scenarios(self, data_line: DataLine):
        assert self._distribution == "DISCRETE"
        assert self._modification == "REPLACE"

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

        if self._state == "STOCH" or self._state == "ENDATA":
            # These are regular sections that have no distribution or
            # modification keywords.
            return res

        if self._state == "SCENARIOS":
            # No other type of scenario is understood (nor given in the
            # standard), so this we can quit early here.
            self._distribution = "DISCRETE"
            self._modification = "REPLACE"
            return True

        distribution = data_line.second_name().upper()
        modification = data_line.third_name().upper()

        if not modification:
            # When not specified, this is the default value (see  Gassmann's
            # notes on the INDEP/BLOCKS sections).
            modification = "REPLACE"

        if modification in _MODIFICATIONS:
            self._modification = modification
        else:
            msg = f"Modification {modification} is not understood."
            logger.error(msg)
            raise ValueError(msg)

        if self._state == "BLOCKS" and distribution in _LINEAR_TRANSFORMATIONS:
            # Linear transformations. These are (AFAIK) only defined for BLOCKS.
            self._distribution = distribution
            return True

        if not distribution:
            msg = f"Distribution not given for {self._state}."
            logger.error(msg)
            raise ValueError(msg)

        if distribution in _DISTRIBUTIONS:
            self._distribution = distribution
        else:
            msg = f"Distribution {distribution} is not understood."
            logger.error(msg)
            raise ValueError(msg)

        return res
