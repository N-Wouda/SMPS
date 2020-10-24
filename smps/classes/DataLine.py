import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class DataLine(ABC):

    def __init__(self, data_line: str):
        data_line = data_line.rstrip()

        logger.debug(f"Creating DataLine('{data_line}').")
        self._raw = data_line

    def is_comment(self) -> bool:
        return len(self._raw) == 0 or self._raw.lstrip().startswith("*")

    def is_header(self) -> bool:
        """
        If True, this DataLine defines a section header. False otherwise.
        """
        return len(self._raw) >= 1 and self._raw[0] not in " *"

    @abstractmethod
    def first_header_word(self):
        raise NotImplementedError

    @abstractmethod
    def has_second_header_word(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def second_header_word(self):
        raise NotImplementedError

    @abstractmethod
    def indicator(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def first_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def second_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def first_number(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def has_third_name(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def third_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def has_second_number(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def second_number(self) -> float:
        raise NotImplementedError

    def raw(self) -> str:
        return self._raw

    def __len__(self) -> int:
        return len(self._raw)

    def __str__(self) -> str:
        return self._raw

    def __repr__(self) -> str:
        return f"DataLine('{self}')"
