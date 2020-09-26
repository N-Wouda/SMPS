from pathlib import Path

from numpy.testing import assert_equal, assert_raises, assert_warns

from smps import SMPS


def test_raises_files_do_not_exist():
    with assert_raises(FileNotFoundError):
        # Weird string that should never exist.
        SMPS("bogus_location/as2afsd76a")

    SMPS("data/electric/LandS")  # this does exist, so should work.


def test_warns_names_disagree():
    with assert_warns(UserWarning):
        SMPS("data/test/different_names")


def test_location():
    """
    Tests if the location property returns the SMPS file location.
    """
    smps = SMPS("data/electric/LandS")
    assert_equal(smps.location, Path("data/electric/LandS"))

# TODO
