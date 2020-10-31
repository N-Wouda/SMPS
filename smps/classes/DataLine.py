import logging

import numpy as np

logger = logging.getLogger(__name__)


class DataLine:
    """
    Parses a single data line in the (S)MPS input, based on the column positions
    explained here: http://tiny.cc/lsyxsz. In particular, the following fields
    are identified:
        - Columns 2 and 3: indicator field,
        - Columns 5-12: first name field,
        - Columns 15-22: second name field,
        - Columns 25-36: first numeric field,
        - Columns 40-47: third data name field,
        - Columns 50-61: second numeric field.

    When a data line is a header, the following is available:
        - Columns 1-14: first word field,
        - Columns 15-72: second word field.

    Arguments
    ---------
    data_line : str
        Raw data line string, to be parsed.

    References
    ----------
    - Birge, J.R., Dempster, M.A.H., Gassmann, H.I., Gunn, E., King, A.J.,
      and Wallace, S.W. 1987. A Standard Input Format for Multiperiod Stochastic
      Linear Programs. `WP-87-118`.
      http://pure.iiasa.ac.at/id/eprint/2934/1/WP-87-118.pdf.
    """

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

    def first_header_word(self):
        return self._raw[0:14].strip()

    def has_second_header_word(self) -> bool:
        return self.second_header_word() != ""

    def second_header_word(self):
        return self._raw[14:72].strip()

    def indicator(self) -> str:
        return self._raw[1:3].strip()

    def first_name(self) -> str:
        return self._raw[4:12].strip()

    def second_name(self) -> str:
        return self._raw[14:22].strip()

    def first_number(self) -> float:
        string = self._raw[24:36].strip()
        return float(string) if len(string) != 0 else float("nan")

    def has_third_name(self) -> bool:
        return self.third_name() != ""

    def third_name(self) -> str:
        return self._raw[39:47].strip()

    def has_second_number(self) -> bool:
        return not np.isnan(self.second_number())

    def second_number(self) -> float:
        string = self._raw[49:61].strip()
        return float(string) if len(string) != 0 else float("nan")

    def raw(self) -> str:
        return self._raw

    def __len__(self) -> int:
        return len(self._raw)

    def __str__(self) -> str:
        return self._raw

    def __repr__(self) -> str:
        return f"DataLine('{self}')"
