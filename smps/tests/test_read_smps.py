from pathlib import Path

from numpy.testing import assert_equal, assert_raises, assert_warns

from smps import read_smps


def test_raises_files_do_not_exist():
    with assert_raises(FileNotFoundError):
        # Weird string that should never exist.
        read_smps("bogus_location/as2afsd76a")

    read_smps("data/electric/LandS")  # this does exist, so should work.


def test_warns_names_disagree():
    with assert_warns(UserWarning):
        read_smps("data/test/different_names")


def test_raises_zero_or_two_locations():
    """
    0 is wrong because, well, what should we read then? 1 is OK, because that
    specifies a triplet of SMPS files without extensions. 2 is wrong, because
    then one file is not specified explicitly. 3 (or more) is OK, because the
    first three files then explicitly specify a set of SMPS files.
    """
    with assert_raises(ValueError):
        read_smps()

    with assert_raises(ValueError):
        read_smps("data/electric/LandS.cor", "data/electric/LandS.tim")


def test_one_location():
    """
    Tests if the location property returns the SMPS file location.
    """
    data = read_smps("data/electric/LandS")

    assert_equal(data.core_location, Path("data/electric/LandS.cor"))
    assert_equal(data.time_location, Path("data/electric/LandS.tim"))
    assert_equal(data.stoch_location, Path("data/electric/LandS.sto"))


def test_three_locations():
    # Three files, but implicit suffix.
    core = Path("data/test/test_explicit_smps_specification_core")
    time = Path("data/test/test_explicit_smps_specification_time")
    stoch = Path("data/test/test_explicit_smps_specification_stoch")

    data = read_smps(core, time, stoch)

    assert_equal(data.core_location, core.with_suffix(".cor"))
    assert_equal(data.time_location, time.with_suffix(".tim"))
    assert_equal(data.stoch_location, stoch.with_suffix(".sto"))

    # Same files, but now explicit with suffix.
    core = core.with_suffix(".cor")
    time = time.with_suffix(".tim")
    stoch = stoch.with_suffix(".sto")

    data = read_smps(core, time, stoch)

    assert_equal(data.core_location, core)
    assert_equal(data.time_location, time)
    assert_equal(data.stoch_location, stoch)


def test_more_than_three_locations():
    # Only the first three arguments (files) are used - the rest is ignored.
    read_smps("data/electric/LandS.cor",
              "data/electric/LandS.tim",
              "data/electric/LandS.sto",
              "data/bogus/bogus",
              "data/bogus/bogus")

# TODO
