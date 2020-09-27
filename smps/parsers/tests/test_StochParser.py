from numpy.testing import assert_raises, assert_warns

from smps.parsers import StochParser


def test_raises_file_does_not_exist():
    with assert_raises(FileNotFoundError):
        StochParser("data/asdf3244325afds/assdew")


def test_warns_missing_stoch_value():
    parser = StochParser("data/test/stoch_missing_stoch_section_value")

    with assert_warns(UserWarning):
        parser.parse()

# TODO
