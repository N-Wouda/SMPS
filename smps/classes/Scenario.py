import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class Scenario:

    def __init__(self,
                 name: str,
                 parent: str,
                 branch_period: str,
                 probability: float):
        logger.debug(f"Creating a Scenario named {name} (parent {parent}),"
                     f" branching in period {branch_period}, with probability"
                     f" {probability}.")

        self._name = name.strip()
        self._parent = parent.strip()
        self._branch_period = branch_period.strip()
        self._probability = probability

        if not (0 < probability < 1):
            msg = "Probabilities outside (0, 1) are not understood."
            logger.error(msg)
            raise ValueError(msg)

        # This stores all modification in this scenario, relative to the parent
        # this scenario branches from.
        self._modifications: List[Tuple[str, str, float]] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> str:
        return self._parent

    @property
    def branch_period(self) -> str:
        return self._branch_period

    @property
    def probability(self) -> float:
        return self._probability

    def add_modification(self, constr: str, var: str, value: float):
        """
        Adds a modification to the scenario.
        """
        self._modifications.append((constr, var, value))
