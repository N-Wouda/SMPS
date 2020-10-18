import pytest
from numpy.testing import assert_almost_equal, assert_equal, assert_raises

from smps.classes import DataLine, Indep
from smps.constants import DISTRIBUTIONS, MODIFICATIONS


@pytest.mark.parametrize("distribution", DISTRIBUTIONS)
def test_raises_strange_distribution_type(distribution):
    """
    Tests if Indep raises when the distribution type is not understood.
    """
    with assert_raises(ValueError):
        Indep("strange distribution")  # not understood

    indep = Indep(distribution)  # should be OK
    assert_equal(indep.distribution, distribution)


@pytest.mark.parametrize("modification", MODIFICATIONS)
def test_raises_strange_modification_type(modification):
    """
    Tests if Indep raises when the distribution type is not understood.
    """
    with assert_raises(ValueError):
        Indep("DISCRETE", "strange modification")  # not understood

    indep = Indep("DISCRETE", modification)  # should be OK
    assert_equal(indep.modification, modification)


@pytest.mark.parametrize("distr,expected", [("DISCRETE", True),
                                            ("NORMAL", False),
                                            ("BETA", False)])
def test_is_finite(distr, expected):
    """
    Tests if ``is_finite()`` returns True for finite (discrete) distributions,
    and False otherwise.
    """
    assert_equal(Indep(distr).is_finite(), expected)


def test_add_distribution():
    """
    Tests if adding a distribution value to an Indep object works.

    TODO test also content, not just length
    TODO parametrize this test
    """
    # Discrete
    line = "    COL1      ROW8      6.0            PERIOD2   0.5"
    data_line = DataLine(line)

    distr = Indep("DISCRETE")

    assert_equal(len(distr), 0)
    distr.add_entry(data_line)
    assert_equal(len(distr), 1)

    # Continuous
    line = "    COL1      ROW8      0.0            PERIOD2   2.0"
    data_line = DataLine(line)

    distr = Indep("NORMAL")

    assert_equal(len(distr), 0)
    distr.add_entry(data_line)
    assert_equal(len(distr), 1)


def test_uniform():
    pass


def test_normal():
    """
    Tests if a discrete section is parsed correctly, and returns an appropriate
    discrete distribution.
    """
    indep = Indep("NORMAL")

    # Inspired by the the LandS stoch file. Normal distribution, as
    # (RHS, DEMAND1) ~ N(mu = 7, sigma^2 = 2)
    data_line = DataLine("    RHS       DEMAND1   7.0            PERIOD2   2")
    indep.add_entry(data_line)

    distr = indep.get_for("RHS", "DEMAND1")

    assert_almost_equal(distr.mean(), 7)
    assert_almost_equal(distr.var(), 2)

    # Since it's a symmetric distribution.
    assert_almost_equal([distr.mean(), distr.median()], [7, 7])


def test_gamma():
    pass


def test_beta():
    pass


def test_lognorm():
    pass


def test_discrete():
    """
    Tests if a discrete section is parsed correctly, and returns an appropriate
    discrete distribution.
    """
    indep = Indep("DISCRETE")

    # First part of the LandS stoch file. Discrete distribution (p_i, x_i), with
    # [(0.3, 3), (0.4, 5), (0.3, 7)].
    lines = ["    RHS       DEMAND1   3.0            PERIOD2   0.3",
             "    RHS       DEMAND1   5.0            PERIOD2   0.4",
             "    RHS       DEMAND1   7.0            PERIOD2   0.3"]

    for line in lines:
        data_line = DataLine(line)
        indep.add_entry(data_line)

    distr = indep.get_for("RHS", "DEMAND1")

    assert_almost_equal(distr.pk, [0.3, 0.4, 0.3])
    assert_almost_equal(distr.xk, [3, 5, 7])
