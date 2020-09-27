from __future__ import annotations

import logging
import warnings
from abc import ABC
from pathlib import Path
from typing import Callable, Dict, Generator, List, Union

from smps.classes import DataLine

logger = logging.getLogger(__name__)


class Parser(ABC):
    """
    Base class for CORE, TIME, and STOCH parsers.

    Arguments
    ---------
    location : Union[str, Path]
        The location to be parsed. This can either be a fully formed file,
        including file extension, or a general location identifying an SMPS
        triplet. In case of the latter, the extension is inferred.

    Raises
    ------
    FileNotFoundError
        When the file pointed to by ``location`` does not exist, or no file
        exists there with appropriate file extension.
    """
    # Accepted file extensions.
    _FILE_EXTENSIONS: List[str] = []

    # Parsing functions for each header section. Since we cannot forward declare
    # these nicely, this dict is a bit ugly in the implementing classes.
    _STEPS: Dict[str, Callable[[Parser, DataLine], None]]

    def __init__(self, location: Union[str, Path]):
        typ = type(self).__name__
        logger.debug(f"Creating {typ} instance with '{location}'.")

        # From Py3.7+ we can rely on insertion order as default behaviour.
        self._state = next(iter(self._STEPS.keys()))
        self._location = Path(location)

        if not self.file_location():
            msg = f"{typ}: {location} does not define an appropriate file."
            logger.error(msg)
            raise FileNotFoundError(msg)

        self._name = ""  # each file defines this field.

    @property
    def name(self) -> str:
        return self._name

    def file_location(self) -> Path:
        """
        Returns a Python path to the file this parser processes. Assumes
        existence has been checked before calling this method.
        """
        if self._location.exists():
            logger.debug(f"Found existing file {self._location}.")
            return self._location

        for extension in self._FILE_EXTENSIONS:
            file = self._location.with_suffix(extension)

            if file.exists():
                logger.debug(f"Found existing file {file}.")
                return file

    def parse(self):
        """
        Parses the given file location.
        """
        for data_line in self._read_file():
            # If any of these conditions is True, this data line is not
            # processed further.
            skip_when = (data_line.is_comment(),
                         self._state == "SKIP",
                         data_line.is_header() and self._transition(data_line))

            if any(skip_when):
                continue

            # This might never get hit as ENDATA is generally the last line of
            # an SMPS file, so the ``continue`` above should end the parse.
            if self._state == "ENDATA":
                break

            func = self._STEPS[self._state]
            func(self, data_line)

    def _read_file(self) -> Generator[DataLine, None, None]:
        """
        Reads the file, one line at a time (generator).

        Yields
        ------
        DataLine
            A DataLine wrapping a single line in the input file.
        """
        with open(str(self.file_location())) as fh:
            for line in fh:
                yield DataLine(line)

    def _transition(self, data_line: DataLine) -> bool:
        """
        Transitions to parsing the next section, defined by this line.

        Parameters
        ----------
        data_line : DataLine
            The section header line.

        Returns
        -------
        bool
            True if after transitioning this line should be skipped, False
            otherwise.
        """
        assert data_line.is_header()
        header = data_line.header()

        if header == self._state:
            # This is very likely the first state, which has a name attribute
            # that should be parsed.
            return False

        if header in self._STEPS or header == "ENDATA":
            logger.info(f"Now parsing the {header} section.")

            self._state = header
            return True

        msg = f"Section {header} is not understood - skipping its entries."
        warnings.warn(msg)
        logger.warning(msg)

        self._state = "SKIP"
        return True
