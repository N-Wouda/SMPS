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
    assert_equal(len(parser.senses), 0)
    assert_equal(len(parser.objective_name), 0)


def test_constraint_rows_lands():
    """
    Tests if the constraints and objective of the LandS problem are correctly
    parsed.
    """
    parser = CoreParser("data/electric/LandS")
    parser.parse()

    # This is pretty much the ROWS section of the LandS problem, excluding the
    # objective ("OBJ").
    values = [('G', "MINCAP"),
              ('L', "BUDGET"),
              ('L', "OPLIM1"),
              ('L', "OPLIM2"),
              ('L', "OPLIM3"),
              ('L', "OPLIM4"),
              ('E', "DEMAND1"),
              ('E', "DEMAND2"),
              ('E', "DEMAND3")]

    senses, names = zip(*values)

    assert_equal(parser.constraint_names, names)
    assert_equal(parser.senses, senses)
    assert_equal(parser.objective_name, "OBJ")


def test_ignore_multiple_no_restriction_rows():
    """
    Tests that in the case multiple rows have "no restriction" (i.e., 'N'), only
    the first is taken for the objective, and any later rows are ignored.
    """
    parser = CoreParser("data/test/core_multiple_no_restriction_rows.cor")
    parser.parse()

    # There are three 'N' rows - the first is names "OBJ1", and should become
    # the objective. All others should be ignored.
    assert_equal(len(parser.constraint_names), 0)
    assert_equal(len(parser.senses), 0)
    assert_equal(parser.objective_name, "OBJ1")

# TODO
