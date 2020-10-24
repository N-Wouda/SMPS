from .DataLine import DataLine


class FreeDataLine(DataLine):

    def __init__(self, data_line: str):
        super().__init__(data_line)
        self._parts = self._raw.strip().split()

    def first_header_word(self):
        assert self.is_header()
        return self._parts[0]  # first item on header line.

    def has_second_header_word(self) -> bool:
        return len(self._parts) > 1

    def second_header_word(self):
        assert self.is_header()
        return self._parts[1]  # second item on header line.

    def indicator(self) -> str:
        pass

    def first_name(self) -> str:
        pass

    def second_name(self) -> str:
        pass

    def first_number(self) -> float:
        pass

    def has_third_name(self) -> bool:
        pass

    def third_name(self) -> str:
        pass

    def has_second_number(self) -> bool:
        pass

    def second_number(self) -> float:
        pass
