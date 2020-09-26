import pytest
from numpy.testing import assert_, assert_almost_equal, assert_equal

from smps.classes import DataLine


@pytest.mark.parametrize("length,string", [(1, "a"), (2, "ab"), (16, "ab" * 8)])
def test_len(length, string):
    """
    Tests if the __len__ function correctly looks at the raw string's length.
    """
    data_line = DataLine(string)
    assert_equal(length, len(data_line))


def test_str():
    """
    Tests if the string representation is sensible.
    """
    data_line = DataLine(" N  OBJ")  # from the LandS.cor file.
    assert_equal(str(data_line), " N  OBJ")


def test_repr():
    """
    Tests if the specific repr implementation is sensible.
    """
    data_line = DataLine(" N  OBJ")  # from the LandS.cor file.
    assert_equal(repr(data_line), "DataLine(' N  OBJ')")


def test_indicator_and_name():
    """
    Tests if the indicator and name are correctly parsed.
    """
    data_line = DataLine(" N  OBJ")  # from the LandS.cor file.

    assert_equal(data_line.indicator(), "N")
    assert_equal(data_line.name(), "OBJ")


def test_comment():
    """
    Tests if the DataLine class correctly detects comment lines.
    """
    data_line = DataLine("* bogus stuff")
    assert_(data_line.is_comment())

    data_line = DataLine("    * BOGUS")
    assert_(data_line.is_comment())

    data_line = DataLine(" N  OBJ")
    assert_(not data_line.is_comment())


def test_first_data_entry():
    """
    Tests if the DataLine class correctly parses the first data entry.
    """
    # From the sslp_5_25_50.cor file.
    line = "    x_1       c2                 188"
    data_line = DataLine(line)

    assert_equal(data_line.name(), "x_1")
    assert_equal(data_line.first_data_name(), "c2")
    assert_almost_equal(data_line.first_number(), 188)


def test_has_no_second_data_entry():
    """
    Tests if the DataLine class correctly determines there is no second data
    entry.
    """
    # From the sslp_5_25_50.cor file.
    line = "    x_1       c2                 188"
    data_line = DataLine(line)

    assert_(not data_line.has_second_data_entry())


def test_second_data_entry():
    """
    Tests if the DataLine class correctly tests if there is a second data entry,
    and parses the result. Also checks that this does not intervene with the
    first data entry.
    """
    # From the sslp_5_25_50.cor file.
    line = "    x_1       obj                 40   c1                  -1"
    data_line = DataLine(line)

    # First data entry
    assert_equal(data_line.name(), "x_1")
    assert_equal(data_line.first_data_name(), "obj")
    assert_almost_equal(data_line.first_number(), 40)

    # Second data entry
    assert_(data_line.has_second_data_entry())
    assert_equal(data_line.second_data_name(), "c1")
    assert_almost_equal(data_line.second_number(), -1)

# TODO
