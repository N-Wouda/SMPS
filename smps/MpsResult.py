from functools import lru_cache
from pathlib import Path
from typing import List

import numpy as np
from scipy.sparse import csr_matrix

from smps.parsers import MpsParser


class MpsResult:
    """
    Parsing result, containing all the data that was read from the MPS file.

    Arguments
    ---------
    mps : MpsParser
        MpsParser instance that was populated with the MPS data.
    """

    def __init__(self, mps: MpsParser):
        self._mps = mps

    @property
    def mps_location(self) -> Path:
        return self._mps.file_location()

    @property
    def name(self) -> str:
        """
        See MpsResult.name.
        """
        return self._mps.name

    @property
    def constraint_names(self) -> List[str]:
        """
        See MpsParser.constraint_names.
        """
        return self._mps.constraint_names

    @property
    def senses(self) -> List[str]:
        """
        See MpsParser.senses.
        """
        return self._mps.senses

    @property
    def rhs(self) -> np.array:
        """
        See MpsParser.coefficients.
        """
        return self._mps.rhs

    @property
    def objective_name(self) -> str:
        """
        See MpsParser.objective_name.
        """
        return self._mps.objective_name

    @property
    @lru_cache(1)
    def coefficients(self) -> csr_matrix:
        """
        See MpsParser.coefficients. This method returns a csr_matrix instead,
        as that is a bit more efficient for most computations.

        Cached after first call.
        """
        return self._mps.coefficients.tocsr()

    @property
    def objective_coefficients(self) -> np.array:
        """
        See MpsParser.objective_coefficients.
        """
        return self._mps.objective_coefficients

    @property
    def variable_names(self) -> List[str]:
        """
        See MpsParser.variable_names.
        """
        return self._mps.variable_names

    @property
    def types(self) -> List[str]:
        """
        See MpsParser.types.
        """
        return self._mps.types

    @property
    def lower_bounds(self) -> np.array:
        """
        See MpsParser.lower_bounds.
        """
        return self._mps.lower_bounds

    @property
    def upper_bounds(self) -> np.array:
        """
        See MpsParser.upper_bounds.
        """
        return self._mps.upper_bounds
