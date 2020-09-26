from numpy.testing import assert_

from smps.parsers import CoreParser


def test_file_exists():
    parser = CoreParser("data/sslp/sslp_5_25_50")
    assert_(parser.file_exists())


def test_file_does_not_exist():
    parser = CoreParser("data/asdf3244325afds/assdew")
    assert_(not parser.file_exists())

# TODO
