from numpy.testing import assert_raises

from smps import SMPS


def test_smps_raises_filenotfounderror():
    with assert_raises(FileNotFoundError):
        # Weird string that should never exist.
        SMPS("bogus_location/as2afsd76a")

    SMPS("data/electric/LandS")  # this does exist, so should work.

# TODO
