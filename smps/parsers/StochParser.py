import logging
import warnings

from smps.classes import DataLine
from .Parser import Parser

logger = logging.getLogger(__name__)


class StochParser(Parser):
    _FILE_EXTENSIONS = [".sto", ".STO", ".stoch", ".STOCH"]
    _STEPS = {
        "STOCH": lambda self, data_line: self._process_stoch(data_line),
        "INDEP": lambda self, data_line: self._process_indep(data_line),
        "BLOCKS": lambda self, data_line: self._process_blocks(data_line),
        "SCENARIOS": lambda self, data_line: self._process_scenarios(data_line),
    }

    def __init__(self, location):
        super().__init__(location)
        # TODO

    def _process_stoch(self, data_line: DataLine):
        assert data_line.header() == "STOCH"

        if len(data_line) > 15:
            self._name = data_line.first_data_name()
        else:
            warnings.warn("Stoch file has no value for the STOCH field.")
            logger.warning("Stoch file has no value for the STOCH field.")

    def _process_indep(self, data_line: DataLine):
        pass  # TODO

    def _process_blocks(self, data_line: DataLine):
        pass  # TODO

    def _process_scenarios(self, data_line: DataLine):
        pass  # TODO

    def _transition(self, data_line):
        res = super()._transition(data_line)
        _, *stoch = data_line.raw().split()

        if self._state in {"INDEP", "BLOCKS", "STOCH"} and len(stoch) != 0:
            pass  # TODO: this indicates the type of stochasticity

        return res
