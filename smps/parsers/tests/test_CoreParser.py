from numpy.testing import assert_, assert_equal, assert_warns

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


def test_warns_and_skips_strange_section():
    parser = CoreParser("data/test/core_file_strange_section")

    with assert_warns(UserWarning):
        parser.parse()

    # There is some data in the STRANGE section, which the parser should have
    # ignored. This makes sure that is indeed the case.
    assert_equal(len(parser.constraint_names), 0)
    assert_equal(len(parser.constraint_senses), 0)
    assert_equal(len(parser.objective_name), 0)

# TODO
