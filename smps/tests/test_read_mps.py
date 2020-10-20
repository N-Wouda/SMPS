from pathlib import Path

import numpy as np
from numpy.testing import assert_almost_equal, assert_equal, assert_raises

from smps import read_mps


def test_raises_file_does_not_exist():
    with assert_raises(FileNotFoundError):
        # Weird string that should not exist.
        read_mps("bogus_location/as2afsd76a")

    read_mps("data/test/mps_test_file_small")  # does exist, so should work.


def test_file_location():
    res = read_mps("data/test/mps_test_file_small")
    assert_equal(res.mps_location, Path("data/test/mps_test_file_small.mps"))


def test_small_example():
    """
    Tests if a small example MPS file is parsed correctly.
    """
    res = read_mps("data/test/mps_test_file_small")

    assert_equal(res.name, "TESTPROB")
    assert_equal(res.constraint_names, ["LIM1", "LIM2", "MYEQN"])
    assert_equal(res.senses, ['L', 'G', 'E'])
    assert_almost_equal(res.rhs, [5, 10, 7])
    assert_equal(res.objective_name, "COST")
    assert_equal(res.variable_names, ["XONE", "YTWO", "ZTHREE"])
    assert_equal(res.types, ['C', 'C', 'C'])
    assert_almost_equal(res.lower_bounds, [0, -1, 0])
    assert_almost_equal(res.upper_bounds, [4, 1, np.inf])

    coefficients = np.array([[1, 1, 0],
                             [1, 0, 1],
                             [0, -1, 1]])
    assert_almost_equal(res.coefficients.toarray(), coefficients)
    assert_almost_equal(res.objective_coefficients, [1, 4, 9])
