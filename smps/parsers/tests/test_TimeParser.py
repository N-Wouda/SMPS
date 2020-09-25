from numpy.testing import assert_

from smps.parsers import TimeParser


def test_time_file_exists():
    parser = TimeParser("data/sslp/sslp_5_25_50")
    assert_(parser.file_exists())


def test_time_file_does_not_exists():
    parser = TimeParser("data/asdf3244325afds/assdew")
    assert_(not parser.file_exists())

# TODO
