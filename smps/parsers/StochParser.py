import logging
import warnings
from typing import Optional

from smps.classes import DataLine, Scenario
from .Parser import Parser

logger = logging.getLogger(__name__)


class StochParser(Parser):
    _file_extensions = [".sto", ".STO", ".stoch", ".STOCH"]
    _steps = {
        "STOCH": lambda self, data_line: self._process_stoch(data_line),
        "INDEP": lambda self, data_line: self._process_indep(data_line),
        "BLOCKS": lambda self, data_line: self._process_blocks(data_line),
        "SCENARIOS": lambda self, data_line: self._process_scenarios(data_line),
    }

    def __init__(self, location):
        super().__init__(location)

        self._type_stoch = ""
        self._scenario: Optional[Scenario] = None
        # TODO

    def _process_stoch(self, data_line: DataLine):
        self._name = data_line.second_header_word()

        if not data_line.second_header_word():
            warnings.warn("Stoch file has no value for the STOCH field.")
            logger.warning("Stoch file has no value for the STOCH field.")

    def _process_indep(self, data_line: DataLine):
        pass  # TODO

    def _process_blocks(self, data_line: DataLine):
        pass  # TODO

    def _process_scenarios(self, data_line: DataLine):
        if data_line.indicator() == "SC":  # new scenario
            scen = Scenario(data_line.name(),
                            data_line.first_data_name(),
                            data_line.second_data_name(),
                            data_line.first_number())

            self._scenario = scen
            return

        var = data_line.name()
        constr = data_line.first_data_name()
        value = data_line.first_number()

        assert self._scenario is not None  # just to be sure
        self._scenario.add_modification(constr, var, value)

        if data_line.has_second_data_entry():
            constr = data_line.second_data_name()
            value = data_line.second_number()

            self._scenario.add_modification(constr, var, value)

    def _transition(self, data_line):
        res = super()._transition(data_line)
        param = data_line.second_header_word().upper()

        if self._state in {"INDEP", "BLOCKS", "STOCH"}:
            if param:
                # TODO param types!
                self._type_stoch = param
            else:
                self._type_stoch = "DISCRETE"

                msg = f"Stoch type was not specified for {self._state};" \
                      f" assuming DISCRETE."

                logger.warning(msg)
                warnings.warn(msg)

        return res
