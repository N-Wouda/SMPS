import logging
import warnings
from collections import defaultdict
from functools import lru_cache
from typing import Dict, List, Tuple

import numpy as np
from scipy.sparse import coo_matrix

from smps.classes import DataLine
from .Parser import Parser

logger = logging.getLogger(__name__)

_BOUNDS_TYPES = {"LO", "UP", "FX", "FR", "MI", "PL", "BV", "LI", "UI"}
_CONSTRAINT_SENSES = {'N', 'L', 'E', 'G'}


class MpsParser(Parser):

    def __init__(self, location):
        super().__init__(location)

        # This list will contain all elements of the constraint matrix, as a
        # list of (constraint, variable, value)-tuples.
        self._elements: List[Tuple[str, str, float]] = []

        # This list contains all objective coefficients, as a list of
        # (variable, value)-tuples.
        self._obj_coeffs: List[Tuple[str, float]] = []
        self._objective_name = ""

        # Constraints.
        self._constr_names: List[str] = []
        self._senses: List[str] = []
        self._rhs: List[float] = []
        self._ranges: Dict[str, Tuple[str, float]] = {}  # name -> (sense, rhs)

        # Variables.
        self._variable_names: List[str] = []
        self._types: List[str] = []
        self._lb: List[float] = []
        self._ub: List[float] = []

        # Look-ups and flags.
        self._constr2idx: Dict[str, int] = {}
        self._var2idx: Dict[str, int] = {}
        self._parse_ints = False  # flag for parsing integers

    @property
    def _file_extensions(self):
        return [".mps", ".MPS"]

    @property
    def _steps(self):
        return {
            "NAME": self._process_name,
            "ROWS": self._process_rows,
            "COLUMNS": self._process_columns,
            "RHS": self._process_rhs,
            "BOUNDS": self._process_bounds,
            "RANGES": self._process_ranges,
        }

    @property
    @lru_cache(1)
    def constraint_names(self) -> List[str]:
        """
        Returns the constraint names, as a list. The first name belongs to the
        first constraint, the second to the second constraint, and so on. This
         list excludes the name of the objective, which can be queried as
        ``objective_name``.

        Names are not unique in case the RANGES data section was present in the
        MPS file (the constraint name is re-used).
        """
        names = self._constr_names.copy()

        for constr in self._ranges:
            names.append(constr)

        return names

    @property
    @lru_cache(1)
    def senses(self) -> List[str]:
        """
        Returns the constraint senses, as a list. The first sense belongs to the
        first constraint, the second to the second constraint, and so on. This
        list contains values in {'E', 'L', 'G'}, indicating equality,
        less-than-equal, or greater-than-equal senses, respectively.
        """
        senses = self._senses.copy()

        for _, (sense, _) in self._ranges.items():
            senses.append(sense)

        return senses

    @property
    @lru_cache(1)
    def rhs(self) -> np.array:
        """
        Constraint right-hand sides, as a vector with one entry per constraint.
        If this was not specified otherwise in the data file, the constraint
        right-hand side defaults to zero.
        """
        rhs = self._rhs.copy()

        for _, (_, value) in self._ranges.items():
            rhs.append(value)

        return np.array(rhs)

    @property
    def objective_name(self) -> str:
        """
        Objective function name.
        """
        return self._objective_name

    @property
    @lru_cache(1)
    def coefficients(self) -> coo_matrix:
        """
        Builds and returns a sparse matrix of the coefficient data. This
        represents the entire tableau, for all stages. Cached after first call.
        """
        data = []
        rows = []
        cols = []

        range_data = defaultdict(list)

        for constr, var, val in self._elements:
            data.append(val)
            rows.append(self._constr2idx[constr])
            cols.append(self._var2idx[var])

            if constr in self._ranges:
                range_data[constr].append((cols[-1], data[-1]))

        range_constr = 0

        for constr, elems in range_data.items():
            idx = len(self._constr2idx) + range_constr
            range_constr += 1

            for var, val in elems:
                data.append(val)
                rows.append(idx)
                cols.append(var)

        shape = (len(self.constraint_names), len(self.variable_names))
        return coo_matrix((data, (rows, cols)), shape=shape)

    @property
    @lru_cache(1)
    def objective_coefficients(self) -> np.array:
        """
        Constructs a dense vector of objective coefficients. Cached after first
        call.
        """
        coeffs = np.zeros(len(self.variable_names))

        for var, val in self._obj_coeffs:
            coeffs[self._var2idx[var]] = val

        return coeffs

    @property
    def variable_names(self) -> List[str]:
        """
        Returns the variable names, as a list. The first name belongs to the
        first variable, the second to the second variable, and so on.
        """
        return self._variable_names

    @property
    def types(self) -> List[str]:
        """
        Returns the variable types, as a list. These types are 'I' for integers,
        'C' for a continuous variable, and 'B' for a binary variable. The first
        type belongs to the first variable, the second to the second variable,
        and so on.
        """
        return self._types

    @property
    def lower_bounds(self) -> np.array:
        """
        Variable lower bounds, as a vector with one entry per variable. If this
        was not specified otherwise in the data file, the lower bound defaults
        to zero.
        """
        return np.array(self._lb)

    @property
    def upper_bounds(self) -> np.array:
        """
        Variable upper bounds, as a vector with one entry per variable. If this
        was not specified otherwise in the data file, the upper bound defaults
        to +infinity.
        """
        return np.array(self._ub)

    def _process_name(self, data_line: DataLine):
        if not data_line.has_second_header_word():
            msg = "MPS file has no value for the NAME field."
            warnings.warn(msg)
            logger.warning(msg)
        else:
            self._name = data_line.second_header_word()

    def _process_rows(self, data_line: DataLine):
        indicator = data_line.indicator()
        name = data_line.first_name()

        assert indicator in _CONSTRAINT_SENSES

        # This is a "no restriction" row, which indicates an objective function.
        # There can be more than one such row, but there can only be one
        # objective. We take the first such row as the objective, and then
        # ignore any subsequent "no restriction" rows.
        if indicator == 'N':
            if self.objective_name == "":
                logger.debug(f"Setting {name} as objective.")
                self._objective_name = name

            return
        else:
            self._constr_names.append(name)
            self._senses.append(indicator)
            self._constr2idx[name] = len(self._constr_names) - 1

    def _process_columns(self, data_line: DataLine):
        name = data_line.second_name()

        if "MARKER" in name.upper():
            self._parse_marker(data_line)
        else:
            self._parse_column(data_line)

    def _process_rhs(self, data_line: DataLine):
        if len(self._rhs) != len(self.constraint_names):
            self._rhs = [0] * len(self.constraint_names)

        self._add_rhs(data_line.second_name(), data_line.first_number())

        if data_line.has_third_name() and data_line.has_second_number():
            self._add_rhs(data_line.third_name(), data_line.second_number())

    def _process_bounds(self, data_line: DataLine):
        """
        There are a ton of bound types, but the most common are listed below,
        originally due to http://lpsolve.sourceforge.net/5.5/mps-format.htm. A
        bound is specified by a two-letter type and a value b.

        - LO    lower bound        b <= x (< +inf)
        - UP    upper bound        (0 <=) x <= b
        - FX    fixed variable     x = b
        - FR    free variable      -inf < x < +inf
        - MI    lower bound -inf   -inf < x (<= 0)
        - PL    upper bound +inf   (0 <=) x < +inf
        - BV    binary variable    x = 0 or 1
        - LI    integer variable   b <= x (< +inf)
        - UI    integer variable   (0 <=) x <= b

        Raises
        ------
        ValueError
            When the bound type is not understood.
        """
        if len(self._lb) != len(self.variable_names):
            self._lb = [0.] * len(self.variable_names)

        if len(self._ub) != len(self.variable_names):
            self._ub = [np.inf] * len(self.variable_names)

        bound_type = data_line.indicator()

        if bound_type not in _BOUNDS_TYPES:
            msg = f"Bounds of type {bound_type} are not understood."
            logger.error(msg)
            raise ValueError(msg)

        var = data_line.second_name()
        idx = self._var2idx[var]

        # The value is clear from the type, and need not have been specified.
        # Hence we treat these separately, and then return.
        if bound_type in {"FR", "MI", "PL", "BV"}:
            if bound_type == "FR":  # free variable
                self._lb[idx] = -np.inf
                self._ub[idx] = np.inf

            if bound_type == "MI":  # -inf lower bound
                self._lb[idx] = -np.inf

            if bound_type == "PL":  # +inf upper bound
                self._ub[idx] = np.inf

            if bound_type == "BV":  # binary variable
                self._lb[idx] = 0
                self._ub[idx] = 1
                self._types[idx] = 'B'

            return

        value = data_line.first_number()

        if bound_type == "LO":  # lower bound
            self._lb[idx] = value

        if bound_type == "UP":  # upper bound
            self._ub[idx] = value

        if bound_type == "FX":  # fixed variable
            self._lb[idx] = value
            self._ub[idx] = value

        if bound_type == "LI":  # integer variable, lower bound
            self._lb[idx] = value
            self._types[idx] = 'I'

        if bound_type == "UI":  # integer variable, upper bound
            self._ub[idx] = value
            self._types[idx] = 'I'

    def _process_ranges(self, data_line: DataLine):
        """
        This is mostly based on the CPLEX manual, and some searching around. See
        also https://github.com/N-Wouda/SMPS/issues/5.
        """
        if len(self._lb) != len(self.variable_names):
            self._lb = [0.] * len(self.variable_names)

        if len(self._ub) != len(self.variable_names):
            self._ub = [np.inf] * len(self.variable_names)

        self._add_range(data_line.second_name(), data_line.first_number())

        if data_line.has_third_name() and data_line.has_second_number():
            self._add_range(data_line.third_name(), data_line.second_number())

    def _add_value(self, constr: str, var: str, value: float):
        if constr == self.objective_name:
            self._obj_coeffs.append((var, value))

        if constr in self._constr2idx:
            self._elements.append((constr, var, value))

        if constr != self.objective_name and constr not in self._constr2idx:
            # This is likely a "no restriction" row other than the objective.
            logger.info(f"Constraint {constr} is not understood; skipping.")

    def _add_rhs(self, constr: str, value: float):
        if constr in self._constr2idx:
            idx = self._constr2idx[constr]
            self._rhs[idx] = value
        else:
            # A right-hand side must be associated with an actual constraint, so
            # this cannot have been a "no restriction" row. It is likely an
            # issue in the MPS file.
            msg = f"Cannot add RHS for unknown constraint {constr}; skipping."
            logger.warning(msg)
            warnings.warn(msg)

    def _add_range(self, constr: str, value: float):
        if constr not in self._constr2idx:
            # A range must be associated with an actual constraint. Here the
            # constraint does not exist, so there is likely an issue with the
            # file.
            msg = f"Cannot add RANGE for unknown constraint {constr}; skipping."
            logger.warning(msg)
            warnings.warn(msg)
            return

        idx = self._constr2idx[constr]
        sense = self._senses[idx]

        # RANGES is for constraints of the form: h <= constraint <= u. The range
        # of the constraint is r = u - h. The value of r is specified in the
        # RANGES section, and the value of u or h is specified in the RHS
        # section. If b is the value entered in the RHS section, and r is the
        # value entered in the RANGES section, then u and h are thus defined:
        #
        #    sense         sign of r       h          u
        #   ----------------------------------------------
        #      G            + or -         b        b + |r|
        #      L            + or -       b - |r|      b
        #      E              +            b        b + |r|
        #      E              -          b - |r|      b
        #
        # (after http://lpsolve.sourceforge.net/5.5/mps-format.htm)
        if sense == 'E':
            if value < 0:
                self._senses[idx] = 'L'
                self._ranges[constr] = ('G', self._rhs[idx] + value)
            else:
                self._senses[idx] = 'G'
                self._ranges[constr] = ('L', self._rhs[idx] + value)

        if sense == 'G':
            self._ranges[constr] = ('L', self._rhs[idx] + abs(value))

        if sense == 'L':
            self._ranges[constr] = ('G', self._rhs[idx] - abs(value))

    def _parse_marker(self, data_line: DataLine):
        assert data_line.has_third_name()

        name = data_line.first_name()
        marker_type = data_line.third_name()

        logger.debug(f"Encountered a {marker_type} marker named {name}.")

        if "INTORG" in marker_type.upper():
            self._parse_ints = True

        if "INTEND" in marker_type.upper():
            self._parse_ints = False

    def _parse_column(self, data_line: DataLine):
        var = data_line.first_name()

        if var not in self._var2idx:
            self._variable_names.append(var)
            self._types.append('I' if self._parse_ints else 'C')
            self._var2idx[var] = len(self._variable_names) - 1

        constr = data_line.second_name()
        value = data_line.first_number()
        self._add_value(constr, var, value)

        if data_line.has_third_name() and data_line.has_second_number():
            constr = data_line.third_name()
            value = data_line.second_number()
            self._add_value(constr, var, value)
