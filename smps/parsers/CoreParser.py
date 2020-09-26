import logging
import warnings
from typing import List, Tuple

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
        self._constr2idx = {}

        self._objective_name = ""

        # This list contains all objective coefficients, as a list of
        # (variable, value)-tuples.
        self._obj_coeffs: List[Tuple[str, float]] = []

        # This list will contain all elements of the constrain matrix, as a list
        # of (constraint, variable, value)-tuples. That's a fairly convenient
        # way to construct the sparse matrices later.
        self._elements: List[Tuple[str, str, float]] = []
        self._variable_names = []
        self._var2idx = {}

        # TODO

    @property
    def constraint_names(self) -> List[str]:
        """
        Returns the constraint names, as a list. The first name belongs to the
        first constraint, the second to the second constraint, and so on. This
         list excludes the name of the objective, which can be queried as
        ``objective_name``.
        """
        return self._constraint_names

    @property
    def constraint_senses(self) -> List[str]:
        """
        Returns the constraint senses, as a list. The first sense belongs to the
        first constraint, the second to the second constraint, and so on. This
        list contains values in {'E', 'L', 'G'}, indicating equality,
        less-than-equal, or greater-than-equal senses, respectively.
        """
        return self._constraint_senses

    @property
    def objective_name(self) -> str:
        """
        Objective function name.
        """
        return self._objective_name

    @property
    def variable_names(self) -> List[str]:
        """
        Returns the variable names, as a list. The first name belongs to the
        first variable, the second to the second variable, and so on.
        """
        return self._variable_names

    def _process_name(self, data_line: DataLine):
        assert data_line.header() == "NAME"

        if len(data_line) > 15:
            self._name = data_line.first_data_name()
        else:
            warnings.warn("Core file has no value for the NAME field.")
            logger.warning("Core file has no value for the NAME field.")

    def _process_rows(self, data_line: DataLine):
        assert data_line.indicator() in set("NELG")

        # This is a "no restriction" row, which indicates an objective function.
        # There can be more than one such row, but there can only be one
        # objective. We take the first such row as the objective, and then
        # ignore any subsequent "no restriction" rows.
        if data_line.indicator() == 'N':
            if self.objective_name == "":
                logger.debug(f"Setting {data_line.name()} as objective.")
                self._objective_name = data_line.name()

            return
        else:
            self._constraint_names.append(data_line.name())
            self._constraint_senses.append(data_line.indicator())

            self._constr2idx[data_line.name()] = len(self._constraint_names) - 1

    def _process_columns(self, data_line: DataLine):
        var = data_line.name()

        if var not in self._var2idx:
            self._variable_names.append(var)
            self._var2idx[var] = len(self._variable_names) - 1

        constr = data_line.first_data_name()
        value = data_line.first_number()
        self._add(constr, var, value)

        if data_line.has_second_data_entry():
            constr = data_line.second_data_name()
            value = data_line.second_number()
            self._add(constr, var, value)

    def _process_rhs(self, data_line: DataLine):
        pass  # TODO

    def _process_bounds(self, data_line: DataLine):
        pass  # TODO

    def _process_ranges(self, data_line: DataLine):
        pass  # TODO

    def _add(self, constr: str, var: str, value: float):
        if constr == self.objective_name:
            self._obj_coeffs.append((var, value))

        if constr in self._constr2idx:
            self._elements.append((constr, var, value))

        if constr != self.objective_name and constr not in self._constr2idx:
            # This is likely a "no restriction" row other than the objective.
            logger.info(f"Constraint {constr} is not understood, and skipped.")
