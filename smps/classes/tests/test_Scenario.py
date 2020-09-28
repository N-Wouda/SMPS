import numpy as np
import pytest
from numpy.testing import (assert_, assert_almost_equal, assert_equal,
                           assert_raises)

from smps.classes import Scenario


@pytest.fixture(autouse=True, scope="function")
def clear_scenarios():
    """
    Clears the global, static scenarios mapping between test runs. This ensures
    each test executes independently.
    """
    Scenario.clear()


@pytest.mark.parametrize("root,outcome", [("'ROOT'", True),
                                          ("ROOT", True),
                                          ("root", True),
                                          ("  'root'  ", True),
                                          ("parent", False)])
def test_parent_is_root(root, outcome):
    scen = Scenario("test", root, "", 0.5)
    assert_equal(scen.branches_from_root(), outcome)


@pytest.mark.parametrize("name,expected", [("test", "test"),
                                           ("test \t\r\n", "test"),
                                           ("  test  ", "test"),
                                           ("te st", "te st")])
def test_name_strips(name, expected):
    """
    Tests if the Scenario class strips the name field of any excess white space.
    """
    scen = Scenario(name, "", "", 0.1)
    assert_equal(scen.name, expected)


@pytest.mark.parametrize("parent_name,read_name", [("parent", "parent"),
                                                   ("parent", "parent  \t\r\n"),
                                                   ("parent", "parent    "),
                                                   ("par ent", "par ent")])
def test_parent_name_strips(parent_name, read_name):
    """
    Tests if the Scenario class strips the parent field of any excess white
    space.
    """
    parent = Scenario(parent_name, "root", "", 0.5)
    scen = Scenario("test", read_name, "", 0.2)
    assert_(scen.parent is parent)


@pytest.mark.parametrize("period,expected", [("test", "test"),
                                             ("test \t\r\n", "test"),
                                             ("  test  ", "test"),
                                             ("te st", "te st")])
def test_branch_period_strips(period, expected):
    """
    Tests if the Scenario class strips the branch period field of any excess
    white space.
    """
    scen = Scenario("", "", period, 0.1)  # regular case
    assert_equal(scen.branch_period, expected)


def test_returns_parent_instance():
    parent = Scenario("parent", "root", "", 0.5)
    scen = Scenario("test", "parent", "", 0.2)

    assert_(parent.parent is None)  # branches from root
    assert_(scen.parent is parent)  # branches from parent


@pytest.mark.parametrize("prob", [0, 1, 10, -1])
def test_raises_probability(prob):
    with assert_raises(ValueError):
        Scenario("", "", "", prob)


@pytest.mark.parametrize("prob", np.linspace(0.001, 0.999, 5))
def test_probability(prob: float):
    scen = Scenario("", "", "", prob)
    assert_almost_equal(scen.probability, prob)


@pytest.mark.parametrize("num_scenarios", [5, 25, 50])
def test_clear(num_scenarios):
    # Creates a number of scenarios - these are not interesting, per se, only
    # that they are properly cleared from the cache once clear() is called.
    [Scenario(f"Scen {idx}", "", "", 1 / num_scenarios)
     for idx in range(num_scenarios)]

    assert_equal(Scenario.num_scenarios(), num_scenarios)

    Scenario.clear()

    assert_equal(Scenario.num_scenarios(), 0)


@pytest.mark.parametrize("num_modifications", [5, 25, 50])
def test_modifications(num_modifications):
    scen = Scenario("test", "", "", 0.5)

    modifications = []

    for idx in range(num_modifications):
        constr = f"Constraint {idx}"
        var = f"Variable {idx}"
        value = idx

        modifications.append((constr, var, value))
        scen.add_modification(constr, var, value)

    assert_equal(scen.modifications, modifications)

# TODO
