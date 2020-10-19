from numpy.testing import assert_equal, assert_raises, assert_warns

from smps.parsers import TimeParser


def test_raises_file_does_not_exist():
    with assert_raises(FileNotFoundError):
        TimeParser("data/asdf3244325afds/assdew")


def test_warns_missing_time_value():
    parser = TimeParser("data/test/time_missing_time_section_value")

    with assert_warns(UserWarning):
        parser.parse()


def test_ignores_data_beyond_endata():
    # This is a correct file with three time periods, for contrast.
    parser = TimeParser("data/test/time_data_before_endata")
    parser.parse()

    assert_equal(parser.name, "Test")
    assert_equal(parser.num_stages, 3)
    assert_equal(parser.time_type, "IMPLICIT")

    # This is the same file, but now the ENDATA field precedes the PERIODS data.
    parser = TimeParser("data/test/time_data_beyond_endata")
    parser.parse()

    assert_equal(parser.name, "Test")
    assert_equal(parser.num_stages, 0)
    assert_equal(parser.time_type, "IMPLICIT")


def test_lands():
    """
    Tests if the LandS time file is parsed correctly.
    """
    parser = TimeParser("data/electric/LandS")
    parser.parse()

    assert_equal(parser.name, "LandS")
    assert_equal(parser.num_stages, 2)
    assert_equal(parser.time_type, "IMPLICIT")

    # X1        MINCAP                   PERIOD1
    # Y11       OPLIM1                   PERIOD2
    assert_equal(parser.implicit_offsets[0], ("X1", "MINCAP"))
    assert_equal(parser.implicit_offsets[1], ("Y11", "OPLIM1"))

    assert_equal(parser.stage_names, ["PERIOD1", "PERIOD2"])


def test_sslp_5_25_50():
    """
    Tests if a small SSLP instance's time file is parsed correctly.
    """
    parser = TimeParser("data/sslp/sslp_5_25_50")
    parser.parse()

    assert_equal(parser.name, "sslp_5_1_25")
    assert_equal(parser.num_stages, 2)
    assert_equal(parser.time_type, "IMPLICIT")

    # x_1       c1                       STAGE-1
    # y_1_1     c2                       STAGE-2
    assert_equal(parser.implicit_offsets[0], ("x_1", "c1"))
    assert_equal(parser.implicit_offsets[1], ("y_1_1", "c2"))

    assert_equal(parser.stage_names, ["STAGE-1", "STAGE-2"])


def test_small_explicit_time_file():
    """
    Tests if a small time file with EXPLICIT periods is parsed correctly.
    """
    parser = TimeParser("data/test/time_small_explicit_problem")
    parser.parse()

    assert_equal(parser.name, "Small explicit problem")
    assert_equal(parser.num_stages, 2)
    assert_equal(parser.time_type, "EXPLICIT")

    #     C1        PERIOD2
    #     C2        PERIOD1
    expected = [("C1", "PERIOD2"), ("C2", "PERIOD1")]
    assert_equal(parser.explicit_constraints, expected)

    #     X1        PERIOD1
    #     X2        PERIOD2
    #     X3        PERIOD1
    expected = [("X1", "PERIOD1"), ("X2", "PERIOD2"), ("X3", "PERIOD1")]
    assert_equal(parser.explicit_variables, expected)

    assert_equal(parser.stage_names, ["PERIOD1", "PERIOD2"])
