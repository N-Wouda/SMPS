from pathlib import Path

from smps.parsers import CoreParser, StochParser, TimeParser


class SmpsResult:
    """
    Parsing result, containing all the data that was read from the SMPS file
    triplet.

    Arguments
    ---------
    core : CoreParser
        CoreParser instance that was populated with the MPS/CORE data.
    time : TimeParser
        TimeParser instance that was populated with the TIME data.
    stoch : StochParser
        StochParser instance that was populated with the STOCH data.
    """

    def __init__(self, core: CoreParser, time: TimeParser, stoch: StochParser):
        self._core = core
        self._time = time
        self._stoch = stoch

    @property
    def core_location(self) -> Path:
        """
        Fully qualified (including extension) path to the CORE file.
        """
        return self._core.file_location()

    @property
    def time_location(self) -> Path:
        """
        Fully qualified (including extension) path to the TIME file.
        """
        return self._time.file_location()

    @property
    def stoch_location(self) -> Path:
        """
        Fully qualified (including extension) path to the STOCH file.
        """
        return self._stoch.file_location()

    # TODO
