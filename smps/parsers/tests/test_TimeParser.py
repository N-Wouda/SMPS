from numpy.testing import assert_, assert_warns

from smps.parsers import TimeParser


def test_time_file_exists():
    parser = TimeParser("data/sslp/sslp_5_25_50")
    assert_(parser.file_exists())


def test_time_file_does_not_exists():
    parser = TimeParser("data/asdf3244325afds/assdew")
    assert_(not parser.file_exists())


def test_warns_missing_time_value():
    parser = TimeParser("data/test/time_file_missing_time_section_value")

    with assert_warns(UserWarning):
        parser.parse()

# TODO
