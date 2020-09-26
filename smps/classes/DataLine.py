import logging

logger = logging.getLogger(__name__)


class DataLine:
    """
    Parses a single data line in the (S)MPS input, based on the column positions
    explained here: http://tiny.cc/lsyxsz. In particular, the following fields
    are identified:
        - Columns 2 and 3: indicator field,
        - Columns 5-12: name field,
        - Columns 15-22: first data name field,
        - Columns 25-36: first numeric field,
        - Columns 40-47: second data name field,
        - Columns 50-61: second numeric field.

    Arguments
    ---------
    data_line : str
        Raw data line string, to be parsed.
    """

    def __init__(self, data_line: str):
        data_line = data_line.rstrip()

        logger.debug(f"Creating DataLine instance with '{data_line}'.")
        self._raw = data_line

    def indicator(self) -> str:
        return self._raw[1:3].strip()

    def is_comment(self) -> bool:
        return self._raw.lstrip().startswith("*")

    def name(self) -> str:
        return self._raw[4:12].strip()

    def first_data_name(self) -> str:
        return self._raw[14:22].strip()

    def first_number(self) -> float:
        return float(self._raw[24:36].strip())

    def has_second_data_entry(self) -> bool:
        # TODO is this sufficient to ensure both the name and number field
        #  exist?
        return len(self._raw) > 40

    def second_data_name(self) -> str:
        return self._raw[39:47].strip()

    def second_number(self) -> float:
        return float(self._raw[49:61].strip())

    def __len__(self) -> int:
        return len(self._raw)

    def __str__(self) -> str:
        return self._raw

    def __repr__(self) -> str:
        return f"DataLine('{self}')"
