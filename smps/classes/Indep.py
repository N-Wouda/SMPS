import logging
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.stats import beta, gamma, lognorm, norm, rv_discrete, uniform

from smps.constants import DISTRIBUTIONS, MODIFICATIONS
from .DataLine import DataLine

logger = logging.getLogger(__name__)


class Indep:
    """
    A single INDEP section, that is, a section of independent random variables.
    Constructed once the header is known, and then populated incrementally
    using ``add_entry``.

    Arguments
    ---------
    distribution : str
        Type of distribution this INDEP section models. One of DISTRIBUTIONS.
    modification : str
        Type of modification relative to the CORE file. One of MODIFICATIONS.
        Default "REPLACE".
    """

    def __init__(self, distribution: str, modification: str = "REPLACE"):
        logger.debug(f"Creating Indep({distribution}, {modification})")

        if modification not in MODIFICATIONS:
            msg = f"Modification {modification} is not understood."
            logger.error(msg)
            raise ValueError(msg)

        if distribution not in DISTRIBUTIONS:
            msg = f"Distribution {distribution} is not understood."
            logger.error(msg)
            raise ValueError(msg)

        self._distribution = distribution
        self._modification = modification

        # These are split because a discrete distribution is constructed
        # value-by-value. Upon return (see get_for()) a scipy.stats discrete
        # distribution is created.
        self._randomness: Dict[Tuple[str, str], Any] = {}
        self._discrete: Dict[Tuple[str, str], List[Tuple[float, float]]] = {}

    @property
    def distribution(self) -> str:
        return self._distribution

    @property
    def modification(self) -> str:
        return self._modification

    def __len__(self) -> int:
        return len(self._randomness) + len(self._discrete)

    def get_for(self, var: str, constr: str):
        """
        Returns the randomness associated with the given variable and
        constraint pair. Returns a ``scipy.stats`` distribution (possibly
        discrete).
        """
        logger.debug(f"Retrieving randomness for ({var}, {constr}).")

        if self.is_finite():
            return rv_discrete(values=zip(*self._discrete[var, constr]))
        else:
            return self._randomness[var, constr]

    def is_finite(self) -> bool:
        """
        Tests if this INDEP section has finite support, or instead stores
        continuous distributions.
        """
        return self._distribution == "DISCRETE"

    def add_entry(self, data_line: DataLine):
        """
        Common interface for adding (new) independent random variables of
        various distributions.
        """
        funcs = {
            "DISCRETE": self.add_discrete,
            "UNIFORM": self.add_uniform,
            "NORMAL": self.add_normal,
            "GAMMA": self.add_gamma,
            "BETA": self.add_beta,
            "LOGNORM": self.add_log_normal,
        }

        func = funcs[self._distribution]
        func(data_line)

    def add_discrete(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        obs = data_line.first_number()
        prob = data_line.second_number()

        if (var, constr) not in self._discrete:
            # Does not use a defaultdict to make sure get_for() always raises
            # a KeyError when (var, constr) is not known.
            self._discrete[var, constr] = []

        self._discrete[var, constr].append((obs, prob))

    def add_uniform(self, data_line: DataLine):
        a = data_line.first_number()
        b = data_line.second_number()

        # We get [a, b], but scipy expects [loc, loc + scale].
        distribution = uniform(loc=a, scale=b - a)

        self._add(data_line, distribution)

    def add_normal(self, data_line: DataLine):
        mean = data_line.first_number()
        var = data_line.second_number()

        # We get the variance, but scipy expects a standard deviation.
        distribution = norm(loc=mean, scale=np.sqrt(var))

        self._add(data_line, distribution)

    def add_gamma(self, data_line: DataLine):
        scale = data_line.first_number()
        shape = data_line.second_number()

        distribution = gamma(shape, scale=scale)

        self._add(data_line, distribution)

    def add_beta(self, data_line: DataLine):
        a = data_line.first_number()
        b = data_line.second_number()

        distribution = beta(a, b)

        self._add(data_line, distribution)

    def add_log_normal(self, data_line: DataLine):
        mean = data_line.first_number()
        var = data_line.second_number()

        # Same as for normal: scipy expects stddev, we get variance.
        distribution = lognorm(loc=mean, scale=np.sqrt(var))

        self._add(data_line, distribution)

    def _add(self, data_line, distribution):
        var = data_line.first_name()
        constr = data_line.second_name()

        self._randomness[var, constr] = distribution

    # TODO sampling/convert discrete indep to scenarios?
