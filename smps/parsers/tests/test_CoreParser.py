import numpy as np
from numpy.testing import (assert_almost_equal, assert_equal,
                           assert_raises, assert_warns)

from smps.parsers import CoreParser


def test_raises_file_does_not_exist():
    with assert_raises(FileNotFoundError):
        CoreParser("data/asdf3244325afds/assdew")


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


def test_matrix_coefficients():
    """
    Tests if the matrix coefficients are parsed correctly on a small file.
    """
    parser = CoreParser("data/test/core_small_problem.cor")
    parser.parse()

    matrix = parser.coefficients.toarray()
    expected = [[1.0, 3.8, 0, 0],
                [2.5, 4.9, 0, 0],
                [18, 1e3, 1.7, 14],
                [0, 16.9, 0, 7.23],
                [0, 0, 0, 0]]

    assert_equal(matrix.shape, (5, 4))
    assert_almost_equal(matrix, expected)


def test_variable_and_constraint_names():
    """
    Tests if the variable and constraint names are parsed correctly on a small
    instance.
    """
    parser = CoreParser("data/test/core_small_problem.cor")
    parser.parse()

    constraints = ["CONSTR1", "CONSTR2", "CONSTR3", "CONSTR4", "OTHER"]
    assert_equal(parser.constraint_names, constraints)

    variables = ["X1", "X2", "X3", "X4"]
    assert_equal(parser.variable_names, variables)


def test_rhs():
    """
    Tests if the RHS coefficients are parsed correctly on a small file.
    """
    parser = CoreParser("data/test/core_rhs.cor")
    parser.parse()

    assert_almost_equal(parser.rhs, [8.0, 5.0, 1e6, 8.0, 12, 0])


def test_rhs_lands():
    """
    Tests if the implementation correctly parses the RHS of the LandS instance.
    """
    parser = CoreParser("data/electric/LandS.cor")
    parser.parse()

    # Only the first two (first-stage) constraints have non-zero RHS specified
    # here - the others follow from the STOCH file and are implicit zero when
    # parsing the CORE file.
    assert_almost_equal(parser.rhs, [14, 120, 0, 0, 0, 0, 0, 0, 0])


def test_rhs_warns_unknown_constraint():
    """
    This core file has an unknown constraint name in the RHS data section. The
    implementation should warn about this.
    """
    parser = CoreParser("data/test/core_unknown_constraint_rhs.cor")

    with assert_warns(UserWarning):
        parser.parse()


def test_parse_bound_types():
    """
    Tests if the parser correctly parses the many available bound types. See
    ``CoreParser._process_bounds`` for an overview of the available types.
    """
    parser = CoreParser("data/test/core_all_bound_types.cor")
    parser.parse()

    #  LO BND       X1        4  [lower bound 4]
    assert_almost_equal(parser.lower_bounds[0], 4)
    assert_almost_equal(parser.upper_bounds[0], np.inf)  # has not been changed
    assert_equal(parser.types[0], 'C')  # has not been changed

    #  UP BND       X2        5  [upper bound 5]
    assert_almost_equal(parser.lower_bounds[1], 0)  # has not been changed
    assert_almost_equal(parser.upper_bounds[1], 5)
    assert_equal(parser.types[1], 'C')  # has not been changed

    #  FX BND       X3        6  [fixed variable at 6]
    assert_almost_equal(parser.lower_bounds[2], 6)
    assert_almost_equal(parser.upper_bounds[2], 6)
    assert_equal(parser.types[2], 'C')  # has not been changed

    #  FR BND       X4  [free variable]
    assert_almost_equal(parser.lower_bounds[3], -np.inf)
    assert_almost_equal(parser.upper_bounds[3], np.inf)
    assert_equal(parser.types[3], 'C')  # has not been changed

    #  MI BND       X5  [lower bound -inf]
    assert_almost_equal(parser.lower_bounds[4], -np.inf)
    assert_almost_equal(parser.upper_bounds[4], np.inf)  # has not been changed
    assert_equal(parser.types[4], 'C')  # has not been changed

    #  PL BND       X6  [upper bound +inf]
    assert_almost_equal(parser.lower_bounds[5], 0)  # has not been changed
    assert_almost_equal(parser.upper_bounds[5], np.inf)
    assert_equal(parser.types[5], 'C')  # has not been changed

    #  BV BND       X7  [binary variable]
    assert_almost_equal(parser.lower_bounds[6], 0)
    assert_almost_equal(parser.upper_bounds[6], 1)
    assert_equal(parser.types[6], 'B')

    #  LI BND       X8        7  [integer variable, lower bound 7]
    assert_almost_equal(parser.lower_bounds[7], 7)
    assert_almost_equal(parser.upper_bounds[7], np.inf)  # has not been changed
    assert_equal(parser.types[7], 'I')

    #  UI BND       X9        8  [integer variable, upper bound 8]
    assert_almost_equal(parser.lower_bounds[8], 0)  # has not been changed
    assert_almost_equal(parser.upper_bounds[8], 8)
    assert_equal(parser.types[8], 'I')


def test_raises_unknown_bound_type():
    """
    Tests if a ValueError is raised when an unknown bound type is encountered in
    the BOUNDS section.
    """
    parser = CoreParser("data/test/core_unknown_bound_type")

    with assert_raises(ValueError):
        parser.parse()

# TODO
