import pytest
from numpy.testing import (assert_, assert_almost_equal, assert_equal)

from smps.classes import DataLine

# These are used to parametrise testing the text fields (i.e., the first,
# second, and third name fields).
_TEXT_TESTS = [("Test1234", "Test1234"),
               ("Test12345", "Test1234"),  # cut-off after 8 characters
               ("Test", "Test"),
               ("Te st", "Te st"),
               (" " * 10 + "DataName", ""),
               ("", "")]

# These are used to parametrise testing the numeric fields (i.e., the first
# and second numeric field).
_NUMERIC_TESTS = [("123.456", 123.456),
                  ("-871.9999", -871.9999),
                  ("0.00", 0),
                  ("1" + "0" * 11, 1e11),
                  ("1" + "0" * 12, 1e11),  # cut-off after 12 characters
                  ("100", 100),
                  (" " * 12, float("nan")),  # curious numpy NaN compare works.
                  ("", float("nan"))]


@pytest.mark.parametrize("length,string", [(1, "a"), (2, "ab"), (16, "ab" * 8)])
def test_len(length, string):
    """
    Tests if the __len__ function correctly looks at the raw string's length.
    """
    data_line = DataLine(string)
    assert_equal(len(data_line), length)


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
    assert_equal(data_line.first_name(), "OBJ")


@pytest.mark.parametrize("line,expected", [("* bogus stuff", True),
                                           ("    * BOGUS", True),
                                           (" N  OBJ", False),
                                           ("", True)])
def test_is_comment(line, expected):
    """
    Tests if the DataLine class correctly detects comment lines.
    """
    data_line = DataLine(line)
    assert_equal(data_line.is_comment(), expected)


@pytest.mark.parametrize("line,expected", [("ROWS", True),
                                           (" N  OBJ", False),
                                           ("* some text", False),
                                           ("*", False),
                                           ("", False)])
def test_is_header(line, expected):
    """
    Tests if the DataLine class correctly detects section headers.
    """
    data_line = DataLine(line)
    assert_equal(data_line.is_header(), expected)


def test_header():
    """
    Tests if the DataLine class correctly parses section headers.
    """
    header_line = DataLine("ROWS")  # empty section header.
    assert_equal(header_line.first_header_word(), "ROWS")

    header_line = DataLine("INDEP         DISCRETE")  # parameterised header.
    assert_equal(header_line.first_header_word(), "INDEP")
    assert_equal(header_line.second_header_word(), "DISCRETE")


def test_first_data_entry():
    """
    Tests if the DataLine class correctly parses the first data entry.
    """
    # From the sslp_5_25_50.cor file.
    line = "    x_1       c2                 188"
    data_line = DataLine(line)

    assert_equal(data_line.first_name(), "x_1")
    assert_equal(data_line.second_name(), "c2")
    assert_almost_equal(data_line.first_number(), 188)


@pytest.mark.parametrize("line,exp_name,exp_number",
                         [("OBJ       10.0", True, True),
                          ("          10.0", False, True),
                          ("OBJ           ", True, False),
                          ("OBJ", True, False),
                          ("              ", False, False),
                          ("", False, False)])
def test_has_second_data_entry(line, exp_name, exp_number):
    """
    Tests if the DataLine class correctly tests if there is a second data
    entry, and parses the result. Also checks that this does not intervene with
    the first data entry.
    """
    padding = " " * 39  # starts at column 40, so 5 spaces.
    data_line = DataLine(padding + line)

    assert_equal(data_line.has_third_name(), exp_name)
    assert_equal(data_line.has_second_number(), exp_number)


@pytest.mark.parametrize("line,expected", [("STOCH", "STOCH"),
                                           ("ROWS   \t\r\n", "ROWS"),
                                           (" N  OBJ", " N  OBJ")])
def test_raw(line, expected):
    """
    Tests if the raw method returns the original string, cleaned for
    line-breaks and the like on the right.
    """
    data_line = DataLine(line)
    assert_equal(data_line.raw(), expected)


@pytest.mark.parametrize("line,expected", [(" XX ", "XX"),
                                           (" Y", "Y"),
                                           ("  Y", "Y"),
                                           (" Y  Name", "Y"),
                                           ("    Name", ""),
                                           ("", "")])
def test_indicator_columns(line, expected):
    """
    The indicator field is the 2-3 column range (inclusive).
    """
    data_line = DataLine(line)
    assert_equal(data_line.indicator(), expected)


@pytest.mark.parametrize("line,expected", _TEXT_TESTS)
def test_first_name_columns(line, expected):
    """
    The first name field is the 5-12 column range (inclusive).
    """
    padding = " " * 4  # starts at column 5, so 4 spaces.
    data_line = DataLine(padding + line)

    assert_equal(data_line.first_name(), expected)


@pytest.mark.parametrize("line,expected", _TEXT_TESTS)
def test_second_name_columns(line, expected):
    """
    The second name field is the 15-12 column range (inclusive).
    """
    padding = " " * 14  # starts at column 15, so 14 spaces.
    data_line = DataLine(padding + line)

    assert_equal(data_line.second_name(), expected)


@pytest.mark.parametrize("line,expected", _NUMERIC_TESTS)
def test_first_number_column(line, expected):
    """
    The first numeric field is the 25-36 column range (inclusive).
    """
    padding = " " * 24  # starts at column 25, so 24 spaces.
    data_line = DataLine(padding + line)

    assert_almost_equal(data_line.first_number(), expected)


@pytest.mark.parametrize("line,expected", _TEXT_TESTS)
def test_third_name_columns(line, expected):
    """
    The third name field is the 40-47 column range (inclusive).
    """
    padding = " " * 39  # starts at column 40, so 39 spaces.
    data_line = DataLine(padding + line)

    assert_equal(data_line.third_name(), expected)


@pytest.mark.parametrize("line,expected", _NUMERIC_TESTS)
def test_second_number_columns(line, expected):
    """
    The second numeric field is the 50-61 column range (inclusive).
    """
    padding = " " * 49  # starts at column 50, so 49 spaces.
    data_line = DataLine(padding + line)

    assert_almost_equal(data_line.second_number(), expected)


@pytest.mark.parametrize("line,expected", [("NAME", "NAME"),
                                           ("NAME  \t\r\n", "NAME"),
                                           ("a" * 15, "a" * 14),
                                           ("a  bc ", "a  bc")])
def test_first_header_word(line, expected):
    """
    The first word field on a header line is the 1-14 column range (inclusive).
    """
    header_line = DataLine(line)

    assert_(header_line.is_header())
    assert_equal(header_line.first_header_word(), expected)


@pytest.mark.parametrize("line,expected", [("Test", "Test"),
                                           ("Test  \t\r\n", "Test"),
                                           ("a" * 59, "a" * 58),
                                           ("a  bc ", "a  bc"),
                                           ("    ab    abc  ", "ab    abc")])
def test_second_header_word(line, expected):
    """
    The second word field on a header line is the 15-72 column range
    (inclusive).
    """
    padding = "NAME" + " " * 10  # second data word starts at column 15.
    header_line = DataLine(padding + line)

    assert_(header_line.is_header())
    assert_equal(header_line.second_header_word(), expected)

# TODO
