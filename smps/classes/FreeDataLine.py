from .DataLine import DataLine
from .ParseContext import ParseContext


class FreeDataLine(DataLine):

    def __init__(self, data_line: str, context: ParseContext):
        super().__init__(data_line)

        self._context = context
        self._parts = self._raw.strip().split()

    def first_header_word(self):
        assert self.is_header()
        return self._parts[0]  # first item on header line.

    def has_second_header_word(self) -> bool:
        return len(self._parts) > 1

    def second_header_word(self):
        assert self.is_header()
        return self._parts[1]  # second item on header line.

    def is_header(self) -> bool:
        return self._context.is_header()

    def indicator(self) -> str:
        assert self._context.has_indicator()
        return self._parts[self._context.indicator_idx()]

    def first_name(self) -> str:
        assert self._context.has_first_name()
        return self._parts[self._context.first_name_idx()]

    def second_name(self) -> str:
        assert self._context.has_second_name()
        return self._parts[self._context.second_name_idx()]

    def first_number(self) -> float:
        assert self._context.has_first_number()
        return self._parts[self._context.first_number_idx()]

    def has_third_name(self) -> bool:
        return self._context.has_third_name()

    def third_name(self) -> str:
        assert self._context.has_third_name()
        return self._parts[self._context.third_name_idx()]

    def has_second_number(self) -> bool:
        return self._context.has_second_number()

    def second_number(self) -> float:
        assert self._context.has_second_number()
        return self._parts[self._context.second_number_idx()]
