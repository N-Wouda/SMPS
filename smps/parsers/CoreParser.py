import logging
import warnings
from typing import List

from smps.classes import DataLine
from .Parser import Parser

logger = logging.getLogger(__name__)


class CoreParser(Parser):
    """
    The core parser essentially parses the MPS part of the SMPS file triplet.
    We follow http://lpsolve.sourceforge.net/5.5/mps-format.htm, and
    http://tiny.cc/lsyxsz.
    """
    FILE_EXTENSIONS = [".cor", ".COR", ".core", ".CORE"]
    STEPS = {
        "NAME": lambda self, data_line: self._process_name(data_line),
        "ROWS": lambda self, data_line: self._process_rows(data_line),
        "COLUMNS": lambda self, data_line: self._process_columns(data_line),
        "RHS": lambda self, data_line: self._process_rhs(data_line),
        "BOUNDS": lambda self, data_line: self._process_bounds(data_line),
        "RANGES": lambda self, data_line: self._process_ranges(data_line),
    }

    def __init__(self, location: str):
        super().__init__(location)

        self._constraint_names = []
        self._constraint_senses = []
        self._objective_name = ""
        # TODO

    @property
    def constraint_names(self) -> List[str]:
        """
        Returns the constraint names, as an ordered list. The first name belongs
        to the first constraint, the second to the second constraint, and so on.
        This list excludes the name of the objective, which can be queried as
        ``objective_name``.
        """
        return self._constraint_names

    @property
    def constraint_senses(self) -> List[str]:
        """
        Returns the constraint senses, as an ordered list. The first sense
        belongs to the first constraint, the second to the second constraint,
        and so on. This list contains values in {'E', 'L', 'G'}, indicating
        equality, less-than-equal, or greater-than-equal senses, respectively.
        """
        return self._constraint_senses

    @property
    def objective_name(self) -> str:
        """
        Objective function name.
        """
        return self._objective_name

    def _process_name(self, data_line: DataLine):
        assert data_line.header() == "NAME"

        if len(data_line) > 15:
            self._name = data_line.first_data_name()
        else:
            warnings.warn("Core file has no value for the NAME field.")
            logger.warning("Core file has no value for the NAME field.")

    def _process_rows(self, data_line: DataLine):
        assert data_line.indicator() in set("NELG")

        # This is a "no restriction" constraint, which indicates an objective
        # function. There can be more than one such constraints, but there can
        # only be one objective. We take the first such row as the objective,
        # and then ignore any subsequent "no restriction" rows.
        if data_line.indicator() == 'N':
            if self.objective_name == "":
                logger.debug(f"Setting {data_line.name()} as objective.")
                self._objective_name = data_line.name()

            return
        else:
            self._constraint_names.append(data_line.name())
            self._constraint_senses.append(data_line.indicator())

    def _process_columns(self, data_line: DataLine):
        pass  # TODO

    def _process_rhs(self, data_line: DataLine):
        pass  # TODO

    def _process_bounds(self, data_line: DataLine):
        pass  # TODO

    def _process_ranges(self, data_line: DataLine):
        pass  # TODO
