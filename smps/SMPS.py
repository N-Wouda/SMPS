import logging
import warnings
from pathlib import Path
from typing import Union

from smps.parsers import CoreParser, StochParser, TimeParser

logger = logging.getLogger(__name__)


class SMPS:
    """
    Parses a triplet of SMPS files.

    Arguments
    ---------
    *locations : Union[str, Path]
        File-system location(s) of the SMPS triplet of files. If only a single
        string is passed, it is assumed this identifies all three files (with
        extensions .cor or .core for the CORE file, .tim or .time for the
        TIME file, and .sto or .stoch for the STOCH file). If (more than) three
        locations are passed, it is assumed the first identifies the CORE file,
        the second the TIME file, and the third the STOCH file. Any remaining
        arguments are ignored.

    Raises
    ------
    FileNotFoundError
        When one of the CORE, TIME, or STOCH files does not exist.
    ValueError
        When a number of locations other than 1 or 3 is received.

    References
    ----------
    See http://lpsolve.sourceforge.net/5.5/mps-format.htm for a detailed
    description of the MPS format (CORE file), and http://tiny.cc/lsyxsz for
    a brief overview of various parts of the other SMPS file.
    """

    def __init__(self, *locations: Union[str, Path]):
        if len(locations) == 1:
            location = Path(locations[0])

            core_location = location
            time_location = location
            stoch_location = location
        elif len(locations) >= 3:
            core_location = Path(locations[0])
            time_location = Path(locations[1])
            stoch_location = Path(locations[2])
        else:
            msg = f"Received {len(locations)} locations, expected 1 or 3."
            logger.error(msg)
            raise ValueError(msg)

        self._core = CoreParser(core_location)
        self._time = TimeParser(time_location)
        self._stoch = StochParser(stoch_location)

        self._core.parse()
        self._time.parse()
        self._stoch.parse()

        if len({self._stoch.name, self._core.name, self._time.name}) != 1:
            msg = "The names in the CORE, TIME, and STOCH files do not agree."
            logger.warning(msg)
            warnings.warn(msg)

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
