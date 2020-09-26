from numpy.testing import assert_, assert_equal, assert_warns

from smps.parsers import TimeParser


def test_file_exists():
    parser = TimeParser("data/sslp/sslp_5_25_50")
    assert_(parser.file_exists())


def test_file_does_not_exist():
    parser = TimeParser("data/asdf3244325afds/assdew")
    assert_(not parser.file_exists())


def test_warns_missing_time_value():
    parser = TimeParser("data/test/time_file_missing_time_section_value")

    with assert_warns(UserWarning):
        parser.parse()


def test_ignores_data_beyond_endata():
    # This is a correct file with three time periods, for contrast.
    parser = TimeParser("data/test/time_file_data_before_endata")
    parser.parse()

    assert_equal(parser.name, "Test")
    assert_equal(len(parser.stage_offsets), 3)

    # This is the same file, but now the ENDATA field precedes the PERIODS data.
    parser = TimeParser("data/test/time_file_data_beyond_endata")
    parser.parse()

    assert_equal(parser.name, "Test")
    assert_equal(len(parser.stage_offsets), 0)

# TODO
