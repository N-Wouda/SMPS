import logging
import warnings

from smps.classes import DataLine
from .Parser import Parser

logger = logging.getLogger(__name__)


class CoreParser(Parser):
    FILE_EXTENSIONS = [".cor", ".COR", ".core", ".CORE"]
    STEPS = {
        "NAME": lambda self, data_line: self._process_name(data_line),
        "ROWS": lambda self, data_line: self._process_rows(data_line),
        "COLUMNS": lambda self, data_line: self._process_columns(data_line),
        "RHS": lambda self, data_line: self._process_rhs(data_line),
        "BOUNDS": lambda self, data_line: self._process_bounds(data_line),
        "RANGES": lambda self, data_line: self._process_ranges(data_line),
    }

    def _process_name(self, data_line: DataLine):
        if len(data_line) > 15:
            self._name = data_line.first_data_name()
        else:
            warnings.warn("Core file has no value for the NAME field.")
            logger.warning("Core file has no value for the NAME field.")

    def _process_rows(self, data_line: DataLine):
        pass  # TODO

    def _process_columns(self, data_line: DataLine):
        pass  # TODO

    def _process_rhs(self, data_line: DataLine):
        pass  # TODO

    def _process_bounds(self, data_line: DataLine):
        pass  # TODO

    def _process_ranges(self, data_line: DataLine):
        pass  # TODO
