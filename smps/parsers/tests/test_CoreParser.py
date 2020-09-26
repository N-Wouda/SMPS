import numpy as np
from numpy.testing import (assert_, assert_almost_equal, assert_equal,
                           assert_raises, assert_warns)

from smps.parsers import CoreParser


def test_file_exists():
    parser = CoreParser("data/sslp/sslp_5_25_50")
    assert_(parser.file_exists())


def test_file_does_not_exist():
    parser = CoreParser("data/asdf3244325afds/assdew")
    assert_(not parser.file_exists())


def test_warns_missing_name_value():
    parser = CoreParser("data/test/core_missing_name_section_value")

    with assert_warns(UserWarning):
        parser.parse()


def test_warns_and_skips_strange_section():
    parser = CoreParser("data/test/core_strange_section")

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


def test_objective_coefficients():
    """
    Tests if the objective coefficients are parsed correctly on a small file.
    """
    parser = CoreParser("data/test/core_objective_coefficients.cor")
    parser.parse()

    assert_almost_equal(parser.objective_coefficients,
                        [10.0, 8, -50.0, 1e3, -18.98, 12.54, 1, 150, 10.0])


def test_objective_coefficients_lands():
    """
    Tests if the objective coefficients are parsed correctly on the LandS
    instance. This is a fairly regular file, without second data entries, and
    no non-zero objectives.
    """
    parser = CoreParser("data/electric/LandS.cor")
    parser.parse()

    expected = [10.0, 7.0, 16.0, 6.0, 40.0, 24.0, 4.0, 45.0, 27.0, 4.5, 32.0,
                19.2, 3.2, 55.0, 33.0, 5.5]

    assert_almost_equal(parser.objective_coefficients,
                        expected)


def test_integer_marker_columns():
    """
    Tests if the implementation correctly parses integer start and end markers.
    """
    parser = CoreParser("data/test/core_integer_markers.cor")
    parser.parse()

    # This example file has two parts that define integer variables. Both
    # should be picked-up correctly.
    assert_equal(parser.types, ['I', 'I', 'C', 'C', 'C', 'I', 'I', 'C'])


def test_rhs():
    """
    TODO
    """
    pass


def test_rhs_lands():
    """
    TODO
    """
    pass


def test_rhs_warns_unknown_constraint():
    """
    TODO
    """
    pass


def test_parse_bound_types():
    """
    Tests if the parser correctly parses the many available bound types. See
    ``CoreParser._process_bounds`` for an overview of the available types.
    """
    parser = CoreParser("data/test/core_all_bound_types.cor")
    parser.parse()

    #  LO BND       X1        4
    assert_almost_equal(parser.lower_bounds[0], 4)
    assert_almost_equal(parser.upper_bounds[0], np.inf)  # has not been changed

    #  UP BND       X2        5
    assert_almost_equal(parser.lower_bounds[1], 0)  # has not been changed
    assert_almost_equal(parser.upper_bounds[1], 5)

    #  FX BND       X3        6
    assert_almost_equal(parser.lower_bounds[2], 6)
    assert_almost_equal(parser.upper_bounds[2], 6)

    #  FR BND       X4
    assert_almost_equal(parser.lower_bounds[3], -np.inf)
    assert_almost_equal(parser.upper_bounds[3], np.inf)

    #  MI BND       X5
    assert_almost_equal(parser.lower_bounds[4], -np.inf)
    assert_almost_equal(parser.upper_bounds[4], np.inf)  # has not been changed

    #  PL BND       X6
    assert_almost_equal(parser.lower_bounds[5], 0)  # has not been changed
    assert_almost_equal(parser.upper_bounds[5], np.inf)

    #  BV BND       X7
    assert_almost_equal(parser.lower_bounds[6], 0)
    assert_almost_equal(parser.upper_bounds[6], 1)
    assert_equal(parser.types[6], 'B')

    #  LI BND       X8        7
    assert_almost_equal(parser.lower_bounds[7], 7)
    assert_almost_equal(parser.upper_bounds[7], np.inf)  # has not been changed
    assert_equal(parser.types[7], 'I')

    #  UI BND       X9        8
    assert_almost_equal(parser.lower_bounds[8], 0)  # has not been changed
    assert_almost_equal(parser.upper_bounds[8], 8)
    assert_equal(parser.types[8], 'I')


def test_raises_unknown_bound_type():
    """
    Tests a ValueError is raised when an unknown bound type is encountered in
    the BOUNDS section.
    """
    parser = CoreParser("data/test/core_unknown_bound_type")

    with assert_raises(ValueError):
        parser.parse()

# TODO
