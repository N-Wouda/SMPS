from numpy.testing import assert_, assert_warns

from smps.parsers import StochParser


def test_file_exists():
    parser = StochParser("data/sslp/sslp_5_25_50")
    assert_(parser.file_exists())


def test_file_does_not_exist():
    parser = StochParser("data/asdf3244325afds/assdew")
    assert_(not parser.file_exists())


def test_warns_missing_stoch_value():
    parser = StochParser("data/test/stoch_file_missing_stoch_section_value")

    with assert_warns(UserWarning):
        parser.parse()

# TODO
