import logging
import warnings
from typing import List, Optional

from smps.classes import DataLine, Indep, Scenario
from .Parser import Parser

logger = logging.getLogger(__name__)


class StochParser(Parser):

    def __init__(self, location):
        super().__init__(location)

        self._current_scen: Optional[Scenario] = None
        self._indep_sections: List[Indep] = []
        # TODO

    @property
    def _file_extensions(self):
        return [".sto", ".STO", ".stoch", ".STOCH"]

    @property
    def _steps(self):
        return {
            "STOCH": self._process_stoch,
            "INDEP": self._process_indep,
            "BLOCKS": self._process_blocks,
            "SCENARIOS": self._process_scenarios,
            "NODES": self._process_nodes,
            "DISTRIB": self._process_distrib,
        }

    @property
    def scenarios(self) -> List[Scenario]:
        return Scenario.scenarios()

    def _process_stoch(self, data_line: DataLine):
        if not data_line.has_second_header_word():
            msg = "Stoch file has no value for the STOCH field."
            warnings.warn(msg)
            logger.warning(msg)
        else:
            self._name = data_line.second_header_word()

    def _process_indep(self, data_line: DataLine):
        assert len(self._indep_sections) >= 1
        indep = self._indep_sections[-1]
        indep.add_entry(data_line)

    def _process_blocks(self, data_line: DataLine):
        pass  # TODO

    def _process_scenarios(self, data_line: DataLine):
        if data_line.indicator() == "SC":  # new scenario
            scen = Scenario(data_line.first_name(),
                            data_line.second_name(),
                            data_line.third_name(),
                            data_line.first_number())

            self._current_scen = scen
            return

        var = data_line.first_name()
        constr = data_line.second_name()
        value = data_line.first_number()

        assert self._current_scen is not None
        self._current_scen.add_modification(constr, var, value)

        if data_line.has_third_name() and data_line.has_second_number():
            constr = data_line.third_name()
            value = data_line.second_number()

            self._current_scen.add_modification(constr, var, value)

    def _process_nodes(self, data_line: DataLine):
        raise NotImplementedError  # TODO maybe at some point in the future

    def _process_distrib(self, data_line: DataLine):
        raise NotImplementedError  # TODO maybe at some point in the future

    def _transition(self, data_line):
        res = super()._transition(data_line)

        if self._state == "STOCH" or self._state == "ENDATA":
            # These are regular sections that have no distribution or
            # modification keywords.
            return res

        if self._state == "SCENARIOS":
            # For SCENARIOS, only DISCRETE and REPLACE are understood (and
            # documented in the manual), so we can quit early here.
            return True

        distr = data_line.second_name().upper()
        mod = data_line.third_name().upper()

        if not mod:
            # When not specified, this is the default value (see Gassmann's
            # notes on the INDEP/BLOCKS sections).
            mod = "REPLACE"

        if not distr:
            msg = f"Distribution not given for {self._state}."
            logger.error(msg)
            raise ValueError(msg)

        if self._state == "INDEP":
            self._indep_sections.append(Indep(distr, mod))

        # TODO make Block/Node?

        return res

    # TODO test is scenarios are finite or have continuous components
