from abc import ABC, abstractmethod
from pathlib import Path


class Parser(ABC):
    FILE_EXTENSIONS = []  # Acceptable file extensions.
    SECTIONS = []  # File sections.

    def __init__(self, location):
        self._location = Path(location)

    def file_exists(self):
        """
        Returns
        -------
        bool
            True if the file location points to a file of the appropriate type
            for this parser, False if not.
        """
        return any((self._location / extension).exists()
                   for extension in self.FILE_EXTENSIONS)

    def file_location(self):
        """
        Returns
        -------
        Path
            A Python path to the file this parser processes. Assumes existence
            has been checked before calling this method.
        """
        for extension in self.FILE_EXTENSIONS:
            if (self._location / extension).exists():
                return self._location / extension

    @abstractmethod
    def parse(self):
        """
        Parses the given file location.
        """
        pass

    def _line(self):
        """
        Parses the file, one line at a time.

        Yields
        ------
        str
            A single line in the input file.
        """
        with open(str(self.file_location())) as fh:
            for line in fh:
                yield line
