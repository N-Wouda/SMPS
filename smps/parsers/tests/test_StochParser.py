from numpy.testing import assert_

from smps.parsers import StochParser


def test_file_exists():
    parser = StochParser("data/sslp/sslp_5_25_50")
    assert_(parser.file_exists())


def test_file_does_not_exist():
    parser = StochParser("data/asdf3244325afds/assdew")
    assert_(not parser.file_exists())

# TODO
