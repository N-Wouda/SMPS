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

    def __init__(self, data_line):
        self._raw = data_line

    def indicator(self):
        return self._raw[1:3].strip()

    def name(self):
        return self._raw[4:12].strip()

    def first_data_name(self):
        return self._raw[14:22].strip()

    def first_number(self):
        return float(self._raw[24:36].strip())

    def has_second_data_entry(self):
        # TODO is this sufficient to ensure both the name and number field
        #  exist?
        return len(self._raw) > 40

    def second_data_name(self):
        return self._raw[39:47].strip()

    def second_number(self):
        return float(self._raw[49:61].strip())

    def __str__(self):
        return self._raw

    def __repr__(self):
        return "DataLine('{raw}')".format(raw=str(self))
