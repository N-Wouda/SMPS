import logging
import warnings

from smps.classes import DataLine
from .Parser import Parser

logger = logging.getLogger(__name__)


class CoreParser(Parser):
    FILE_EXTENSIONS = [".cor", ".COR", ".core", ".CORE"]
    STEPS = {
        "NAME": lambda self, data_line: self._process_name(data_line),
        "ROWS": lambda self, data_line: None,  # TODO
        "COLUMNS": lambda self, data_line: None,  # TODO
        "RHS": lambda self, data_line: None,  # TODO
        "BOUNDS": lambda self, data_line: None,  # TODO
        "RANGES": lambda self, data_line: None,  # TODO
    }

    def _process_name(self, data_line: DataLine):
        if len(data_line) > 15:
            self._name = data_line.first_data_name()
        else:
            warnings.warn("Core file has no value for the NAME field.")
            logger.warning("Core file has no value for the NAME field.")
