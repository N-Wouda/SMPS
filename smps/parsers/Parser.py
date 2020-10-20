import logging
import warnings
from abc import ABC
from pathlib import Path
from typing import Callable, Dict, Generator, List, Optional, Union

from smps.classes import DataLine, FixedDataLine, FreeDataLine

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
    _is_fixed: bool = True  # type of file parsed (free or fixed).
    _file_extensions: List[str] = []  # accepted file extensions.

    # Parsing functions for each header section. Since we cannot forward declare
    # these nicely, this dict is a bit ugly in the implementing classes.
    _steps: Dict[str, Callable[["Parser", DataLine], None]]

    def __init__(self, location: Union[str, Path]):
        typ = type(self).__name__
        logger.debug(f"Creating {typ}('{location}').")

        # Insertion order is a CPython implementation detail in Py3.6, but from
        # Py3.7+ we can rely on insertion order as default behaviour.
        self._state = next(iter(self._steps.keys()))
        self._location = Path(location)

        if self.file_location() is None:
            msg = f"{typ}: {location} does not define an appropriate file."
            logger.error(msg)
            raise FileNotFoundError(msg)

        self._name = ""  # each file defines this field.

    @property
    def name(self) -> str:
        return self._name

    def file_location(self) -> Optional[Path]:
        """
        Returns a Python path to the file this parser processes. Assumes
        existence has been checked before calling this method. Returns None
        if the file could not be found.
        """
        if self._location.exists():
            logger.debug(f"Found existing file {self._location}.")
            return self._location

        for extension in self._file_extensions:
            file = self._location.with_suffix(extension)

            if file.exists():
                logger.debug(f"Found existing file {file}.")
                return file

        return None

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

            func = self._steps[self._state]
            func(self, data_line)

    @classmethod
    def set_fixed(cls):
        cls._is_fixed = True

    @classmethod
    def set_free(cls):
        cls._is_fixed = False

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
                if self._is_fixed:
                    yield FixedDataLine(line)
                else:
                    yield FreeDataLine(line)

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
        header = data_line.first_header_word()

        if header == self._state:
            # This is the initial state, which has a name attribute that should
            # be parsed.
            return False

        if header in self._steps or header == "ENDATA":
            logger.info(f"Now parsing the {header} section.")

            self._state = header
            return True

        msg = f"Section {header} is not understood - skipping its entries."
        warnings.warn(msg)
        logger.warning(msg)

        self._state = "SKIP"
        return True
