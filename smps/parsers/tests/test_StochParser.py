import pytest
from numpy.testing import (assert_almost_equal, assert_equal,
                           assert_raises, assert_warns)

from smps.classes import Scenario
from smps.parsers import StochParser


def _compare_scenarios(actual: Scenario, desired: Scenario):
    """
    Helper method for tests that need to compare scenarios by their values.
    """
    assert_equal(actual.name, desired.name)
    assert_equal(actual.branch_period, desired.branch_period)
    assert_almost_equal(actual.probability, desired.probability)

    for des, act in zip(desired.modifications, actual.modifications):
        assert_equal(act.constraint, des.constraint)
        assert_equal(act.variable, des.variable)
        assert_almost_equal(act.value, des.value)


def test_raises_file_does_not_exist():
    with assert_raises(FileNotFoundError):
        StochParser("data/asdf3244325afds/assdew")


def test_raises_non_discrete_scenarios():
    """
    If the parser detects a SCENARIOS header, those *must* be DISCRETE, and not
    something else.
    """
    with assert_raises(ValueError):
        parser = StochParser("data/test/stoch_non_discrete_scenarios")
        parser.parse()


def test_warns_missing_stoch_value():
    parser = StochParser("data/test/stoch_missing_stoch_section_value")

    with assert_warns(UserWarning):
        parser.parse()


def test_warns_missing_stochasticity_parameter():
    """
    When an INDEP, BLOCKS, or SCENARIOS section is first encountered a second
    header word is expected, which explains the type of stochasticity. When this
    is missing, it defaults to DISCRETE and should issue a warning.
    """
    parser = StochParser('data/test/stoch_no_stochasticity_parameter')

    with assert_warns(UserWarning):
        parser.parse()


@pytest.mark.usefixtures("clear_scenarios")
def test_parses_scenarios_sizes3():
    """
    Tests if the scenarios of the small sizes3.sto are parsed correctly.
    """
    parser = StochParser("data/sizes/sizes3")
    parser.parse()

    assert_equal(len(parser.scenarios), 3)

    # Full first scenario of the sizes3.sto file.
    desired = Scenario("SCEN01", "ROOT", "STAGE-2", 0.333333)
    desired.add_modification("D01JJ02", "RHS", 1.750)
    desired.add_modification("D02JJ02", "RHS", 5.250)
    desired.add_modification("D03JJ02", "RHS", 8.750)
    desired.add_modification("D04JJ02", "RHS", 7.000)
    desired.add_modification("D05JJ02", "RHS", 24.500)
    desired.add_modification("D06JJ02", "RHS", 17.500)
    desired.add_modification("D07JJ02", "RHS", 10.500)
    desired.add_modification("D08JJ02", "RHS", 8.750)
    desired.add_modification("D09JJ02", "RHS", 8.750)
    desired.add_modification("D10JJ02", "RHS", 3.500)

    _compare_scenarios(parser.scenarios[0], desired)


@pytest.mark.usefixtures("clear_scenarios")
def test_parses_scenarios_small_instance():
    """
    Tests if the parser correctly reads the scenarios of a small test instance.
    """
    parser = StochParser("data/test/stoch_small_scenarios_problem.sto")
    parser.parse()

    assert_equal(len(parser.scenarios), 2)

    #  SC SCEN01    ROOT      0.333333       STAGE-2
    #     RHS       C1        1              C2        5.0001
    #     X1        C1        5
    first = Scenario("SCEN01", "ROOT", "STAGE-2", 0.333333)
    first.add_modification("C1", "RHS", 1)
    first.add_modification("C2", "RHS", 5.001)
    first.add_modification("C1", "RHS", 5)

    _compare_scenarios(parser.scenarios[0], first)

    #  SC SCEN02    SCEN01    0.666667       STAGE-3
    #     RHS       C1        8
    #     X2        C2        7
    second = Scenario("SCEN02", "SCEN01", "STAGE-3", 0.666667)
    second.add_modification("C1", "RHS", 8)
    second.add_modification("C1", "X2", 7)

    _compare_scenarios(parser.scenarios[1], second)

# TODO
