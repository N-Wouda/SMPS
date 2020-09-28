import pytest

from smps.classes import Scenario


@pytest.fixture
def clear_scenarios():
    """
    Clears the global, static scenarios mapping between test runs. This ensures
    each test executes independently.
    """
    Scenario.clear()  # before test
    yield
    Scenario.clear()  # after test
