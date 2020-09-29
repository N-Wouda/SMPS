from collections import defaultdict

import numpy as np
from scipy.stats import (beta, gamma, lognorm, multivariate_normal, norm,
                         uniform)

from .DataLine import DataLine


class Indep:

    def __init__(self):
        self._randomness = {}
        self._discrete = defaultdict(list)

    def add_entry(self, typ: str, data_line: DataLine):
        funcs = {
            "DISCRETE": self.add_discrete,
            "UNIFORM": self.add_uniform,
            "NORMAL": self.add_normal,
            "GAMMA": self.add_gamma,
            "BETA": self.add_beta,
            "LOGNORM": self.add_log_normal,
            "MVNORMAL": self.add_mv_normal,
        }

        func = funcs[typ]
        func(data_line)

    def add_discrete(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        obs = data_line.first_number()
        prob = data_line.second_number()

        self._discrete[constr, var].append((obs, prob))

    def add_uniform(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        a = data_line.first_number()
        b = data_line.second_number()

        # uniform(loc, scale) == Uniform[loc, loc + scale].
        self._randomness[constr, var] = uniform(loc=a, scale=b - a)

    def add_normal(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        a = data_line.first_number()
        b = data_line.second_number()

        # norm(loc, scale) == Normal[loc, scale ** 2).
        self._randomness[constr, var] = norm(loc=a, scale=np.sqrt(b))

    def add_gamma(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        a = data_line.first_number()
        b = data_line.second_number()

        # TODO
        self._randomness[constr, var] = gamma()

    def add_beta(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        a = data_line.first_number()
        b = data_line.second_number()

        # TODO
        self._randomness[constr, var] = beta()

    def add_log_normal(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        a = data_line.first_number()
        b = data_line.second_number()

        # TODO
        self._randomness[constr, var] = lognorm()

    def add_mv_normal(self, data_line: DataLine):
        var = data_line.first_name()
        constr = data_line.second_name()

        a = data_line.first_number()
        b = data_line.second_number()

        # TODO
        self._randomness[constr, var] = multivariate_normal()
