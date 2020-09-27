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


def test_parent_is_root():
    # This is the regular scenario.
    scen = Scenario("test", "'ROOT'", "", 0.1)
    assert_(scen.branches_from_root())

    # Root is sometimes given with or without the quotes, or not in uppercase.
    scen = Scenario("test", "root", "", 0.1)
    assert_(scen.branches_from_root())

    # Tests if padding is stripped correctly.
    scen = Scenario("test", "  'root'  ", "", 0.1)
    assert_(scen.branches_from_root())

    # This scenario has a regular parent, which is not root.
    scen = Scenario("test", "parent", "", 0.1)
    assert_(not scen.branches_from_root())


def test_name_strips():
    """
    Tests if the Scenario class strips the name field of any excess white space.
    """
    scen = Scenario("test", "", "", 0.1)  # regular case
    assert_equal(scen.name, "test")

    scen = Scenario("test  \t\r\n", "", "", 0.1)  # lots of stuff to the right
    assert_equal(scen.name, "test")

    scen = Scenario("  test   ", "", "", 0.1)  # padding on both ends
    assert_equal(scen.name, "test")

    scen = Scenario("te st", "", "", 0.1)  # this is *not* padding
    assert_equal(scen.name, "te st")


def test_parent_name_strips():
    """
    Tests if the Scenario class strips the parent field of any excess white
    space.
    """
    parent = Scenario("parent", "root", "", 0.5)
    scen = Scenario("test", "parent", "", 0.2)
    assert_(scen.parent is parent)  # regular case

    parent = Scenario("parent", "root", "", 0.5)
    scen = Scenario("test", "parent  \t\r\n", "", 0.2)
    assert_(scen.parent is parent)  # lots of stuff to the right

    parent = Scenario("parent", "root", "", 0.5)
    scen = Scenario("test", "  parent   ", "", 0.2)
    assert_(scen.parent is parent)  # padding on both ends

    parent = Scenario("par ent", "root", "", 0.5)
    scen = Scenario("test", "par ent", "", 0.2)
    assert_(scen.parent is parent)  # this is *not* padding


def test_branch_period_strips():
    """
    Tests if the Scenario class strips the branch period field of any excess
    white space.
    """
    scen = Scenario("", "", "test", 0.1)  # regular case
    assert_equal(scen.branch_period, "test")

    scen = Scenario("", "", "test  \t\r\n", 0.1)  # lots of stuff to the right
    assert_equal(scen.branch_period, "test")

    scen = Scenario("", "", "  test   ", 0.1)  # padding on both ends
    assert_equal(scen.branch_period, "test")

    scen = Scenario("", "", "te st", 0.1)  # this is *not* padding
    assert_equal(scen.branch_period, "te st")


def test_returns_parent_instance():
    parent = Scenario("parent", "root", "", 0.5)
    scen = Scenario("test", "parent", "", 0.2)

    assert_(parent.parent is None)  # branches from root
    assert_(scen.parent is parent)  # branches from parent


def test_raises_probability():
    with assert_raises(ValueError):
        Scenario("", "", "", 0)  # zero probability

    with assert_raises(ValueError):
        Scenario("", "", "", 1)  # unit probability

    with assert_raises(ValueError):
        Scenario("", "", "", 10)  # far outside unit interval

    with assert_raises(ValueError):
        Scenario("", "", "", -1)  # negative probability

    for prob in np.linspace(0.001, 0.999, 100):  # should all be fine
        scen = Scenario("", "", "", prob)
        assert_almost_equal(scen.probability, prob)


def test_clear():
    for num_scenarios in [5, 25, 50]:
        # Creates a number of scenarios - these are not interesting, per se,
        # only that they are properly cleared from the cache once clear() is
        # called.
        [Scenario(f"Scen {idx}", "", "", 1 / num_scenarios)
         for idx in range(num_scenarios)]

        assert_equal(Scenario.num_scenarios(), num_scenarios)

        Scenario.clear()

        assert_equal(Scenario.num_scenarios(), 0)

# TODO
