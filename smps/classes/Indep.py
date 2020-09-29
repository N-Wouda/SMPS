from collections import defaultdict
from typing import Any, Dict, Tuple

import numpy as np
from scipy.stats import (beta, gamma, lognorm, multivariate_normal, norm,
                         uniform)

from .DataLine import DataLine


class Indep:
    """
    A single INDEP section, that is, a section of independent random variables.
    Constructed once the header is known, and then populated incrementally
    using ``add_entry``.

    Arguments
    ---------
    distribution : str
        Type of distribution this INDEP section models. One of {"DISCRETE",
        "UNIFORM", "NORMAL", "GAMMA", "BETA", "LOGNORM", "MVNORMAL"}.
    modification : str
        Type of modification relative to the CORE file. One of {"ADD",
        "MULTIPLY", "REPLACE"}. Default "REPLACE".
    """

    def __init__(self, distribution: str, modification: str = "REPLACE"):
        self._distribution = distribution
        self._modification = modification

        self._randomness: Dict[Tuple[str, str], Any] = {}
        self._discrete = defaultdict(list)

    def add_entry(self, data_line: DataLine):
        """
        Common interface for adding many types of distributions to the
        """
        funcs = {
            "DISCRETE": self.add_discrete,
            "UNIFORM": self.add_uniform,
            "NORMAL": self.add_normal,
            "GAMMA": self.add_gamma,
            "BETA": self.add_beta,
            "LOGNORM": self.add_log_normal,
            "MVNORMAL": self.add_mv_normal,
        }

        func = funcs[self._distribution]
        func(data_line)

    def add_discrete(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        obs = data_line.first_number()
        prob = data_line.second_number()

        self._discrete[constr, var].append((obs, prob))

    def add_uniform(self, data_line: DataLine):
        a = data_line.first_number()
        b = data_line.second_number()

        distribution = uniform(loc=a, scale=b - a)

        self._add(data_line, distribution)

    def add_normal(self, data_line: DataLine):
        mean = data_line.first_number()
        var = data_line.second_number()

        distribution = norm(loc=mean, scale=np.sqrt(var))

        self._add(data_line, distribution)

    def add_gamma(self, data_line: DataLine):
        a = data_line.first_number()
        b = data_line.second_number()

        distribution = gamma()  # TODO

        self._add(data_line, distribution)

    def add_beta(self, data_line: DataLine):
        a = data_line.first_number()
        b = data_line.second_number()

        distribution = beta()  # TODO

        self._add(data_line, distribution)

    def add_log_normal(self, data_line: DataLine):
        a = data_line.first_number()
        b = data_line.second_number()

        distribution = lognorm()  # TODO

        self._add(data_line, distribution)

    def add_mv_normal(self, data_line: DataLine):
        a = data_line.first_number()
        b = data_line.second_number()

        distribution = multivariate_normal()  # TODO

        self._add(data_line, distribution)

    def _add(self, data_line, distribution):
        var = data_line.first_name()
        constr = data_line.second_name()

        self._randomness[constr, var] = distribution
