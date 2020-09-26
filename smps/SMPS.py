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
    location : str, Path
        File-system location of the SMPS triplet of files. Assumes these files
        have extensions .cor or .core for the CORE file, .tim or .time for the
        TIME file, and .sto or .stoch for the STOCH file.

    Raises
    ------
    FileNotFoundError
        When one of the CORE, TIME, or STOCH files does not exist.
    """

    def __init__(self, location: Union[str, Path]):
        # TODO allow specifying different locations for each file (i.e. 3, not
        #  1 overall).
        self._location = Path(location)

        self._core = CoreParser(location)
        self._time = TimeParser(location)
        self._stoch = StochParser(location)

        parsers = [self._core, self._time, self._stoch]

        if not all(parser.file_exists() for parser in parsers):
            raise FileNotFoundError("One of the CORE, TIME, or STOCH files does"
                                    " not exist.")

        self._core.parse()
        self._time.parse()
        self._stoch.parse()

        if len({self._stoch.name, self._core.name, self._time.name}) != 1:
            msg = "The names in the CORE, TIME, and STOCH files do not agree."
            logger.warning(msg)
            warnings.warn(msg)

    @property
    def location(self) -> Path:
        """
        Returns the file-system location of the SMPS triplet of files, without
        any extensions.

        Returns
        -------
        Path
            The location, as a Python path.
        """
        return self._location

    # TODO
