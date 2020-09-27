from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class Scenario:
    # Mapping of all scenarios by name. This is used to look-up any parent
    # scenarios.
    _SCENARIOS: Dict[str, Scenario] = {}

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
        Scenario._SCENARIOS[self._name] = self

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Optional[Scenario]:
        """
        Returns the parent scenario, or None if this scenario branches from
        root.
        """
        if self.branches_from_root():
            return None

        return Scenario._SCENARIOS[self._parent]

    @property
    def branch_period(self) -> str:
        return self._branch_period

    @property
    def probability(self) -> float:
        return self._probability

    def add_modification(self, constr: str, var: str, value: float):
        """
        Adds a modification to the scenario. This is a modification relative
        to the parent scenario.
        """
        self._modifications.append((constr, var, value))

    def branches_from_root(self) -> bool:
        """
        True if this scenario branches from ROOT, that is, directly from the
        core file.
        """
        return "ROOT" in self._parent.upper()

    @classmethod
    def clear(cls):
        """
        Empties the stored scenario mapping (cache).
        """
        cls._SCENARIOS.clear()

    @classmethod
    def num_scenarios(cls) -> int:
        """
        Returns the number of scenarios stored in cache.
        """
        return len(cls._SCENARIOS)
