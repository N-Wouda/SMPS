from numpy.testing import assert_, assert_warns

from smps.parsers import CoreParser


def test_file_exists():
    parser = CoreParser("data/sslp/sslp_5_25_50")
    assert_(parser.file_exists())


def test_file_does_not_exist():
    parser = CoreParser("data/asdf3244325afds/assdew")
    assert_(not parser.file_exists())


def test_warns_missing_name_value():
    parser = CoreParser("data/test/core_file_missing_name_section_value")

    with assert_warns(UserWarning):
        parser.parse()

# TODO
