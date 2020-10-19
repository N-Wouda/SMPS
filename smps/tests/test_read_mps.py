from pathlib import Path

from numpy.testing import assert_equal, assert_raises

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
    # TODO
