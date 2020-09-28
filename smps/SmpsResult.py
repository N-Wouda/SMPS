from pathlib import Path
from dataclasses import dataclass
from smps.parsers import CoreParser, StochParser, TimeParser


@dataclass
class SmpsResult:
    """
    Parsing result, containing all the data that was read from the SMPS file
    triplet.
    """
    _core: CoreParser
    _time: TimeParser
    _stoch: StochParser

    @property
    def core_location(self) -> Path:
        return self._core.file_location()

    @property
    def time_location(self) -> Path:
        return self._time.file_location()

    @property
    def stoch_location(self) -> Path:
        return self._stoch.file_location()

    # TODO
