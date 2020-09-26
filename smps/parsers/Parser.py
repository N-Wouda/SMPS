from __future__ import annotations

import logging
from abc import ABC
from pathlib import Path
from typing import Callable, Dict, Generator, List, Union

from smps.classes import DataLine

logger = logging.getLogger(__name__)


class Parser(ABC):
    # Accepted file extensions.
    FILE_EXTENSIONS: List[str] = []

    # Parsing functions for each header section. Since we cannot forward declare
    # these nicely, this dict is a bit ugly in the implementing classes.
    STEPS: Dict[str, Callable[[Parser, DataLine], None]]

    def __init__(self, location: Union[str, Path]):
        logger.debug(f"Creating Parser instance with '{location}'.")

        # From Py3.7+ we can rely on insertion order as default behaviour.
        self._state = next(iter(self.STEPS.keys()))
        self._location = Path(location)

        self._name = ""  # each file defines this field.

    @property
    def name(self) -> str:
        return self._name

    def file_exists(self) -> bool:
        """
        Returns
        -------
        bool
            True if the file location points to a file of the appropriate type
            for this parser, False if not.
        """
        return any(self._location.with_suffix(extension).exists()
                   for extension in self.FILE_EXTENSIONS)

    def file_location(self) -> Path:
        """
        Returns
        -------
        Path
            A Python path to the file this parser processes. Assumes existence
            has been checked before calling this method.

        Raises
        ------
        AssertionError
            When the file does not exist.
        """
        assert self.file_exists()

        for extension in self.FILE_EXTENSIONS:
            file = self._location.with_suffix(extension)

            if file.exists():
                logger.debug(f"Found existing file {file}.")
                return file

    def parse(self):
        """
        Parses the given file location.
        """
        for line in self._line():
            data_line = DataLine(line)

            if data_line.is_comment() or self._transition(line):
                continue

            # This will likely never get hit, as ENDATA is generally the last
            # line of an SMPS file. Nonetheless, it signals end of parsing, no
            # matter what follows.
            if self._state == "ENDATA":
                break

            func = self.STEPS[self._state]
            func(self, data_line)

    def _line(self) -> Generator[str, None, None]:
        """
        Reads the file, one line at a time (generator).

        Yields
        ------
        str
            A single line in the input file.
        """
        with open(str(self.file_location())) as fh:
            for line in fh:
                yield line

    def _transition(self, line: str) -> bool:
        """
        Checks if the passed-in line defines a section header, in which case
        we are about to parse a new part of the file.

        Parameters
        ----------
        line : str
            The line to test.

        Returns
        -------
        bool
            True if this line is a section header, False otherwise.
        """
        # Some sections has additional definitions in their header. Here we
        # care only about the first value.
        parts = line.strip().split()
        clean = parts[0].upper()

        if clean == self._state:
            return False  # this is very likely the first state.

        if clean in self.STEPS or clean == "ENDATA":
            logger.info(f"Now parsing the {clean} section.")
            self._state = clean
            return True

        return False
