from abc import ABC, abstractmethod
from pathlib import Path


class Parser(ABC):
    FILE_EXTENSIONS = []  # Acceptable file extensions for this parser.

    def __init__(self, location):
        self._location = location

    def file_exists(self):
        """
        Returns
        -------
        bool
            True if the file location points to a file of the appropriate type
            for this parser, False if not.
        """
        return any(Path(self._location / extension).exists()
                   for extension in self.FILE_EXTENSIONS)

    @abstractmethod
    def parse(self):
        """
        Parses the given file location.
        """
        pass
