from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator, List, Union

from smps.classes import DataLine


class Parser(ABC):
    FILE_EXTENSIONS: List[str] = []  # Acceptable file extensions.
    SECTIONS: List[str] = []  # Header (file) sections.

    def __init__(self, location: Union[str, Path]):
        self._location = Path(location)

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
            if self._location.with_suffix(extension).exists():
                return self._location.with_suffix(extension)

    def parse(self):
        """
        Parses the given file location.
        """
        for line in self._line():
            data_line = DataLine(line)

            if data_line.is_comment() or self._transition(line):
                continue

            self._process_data_line(data_line)

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

    @abstractmethod
    def _process_data_line(self, data_line: DataLine):
        """
        Processes the given data line.

        Parameters
        ----------
        data_line : DataLine
            A single line in the file that's being parsed.
        """
        pass  # no-op, implementation in concrete implementations

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
        pass  # TODO
