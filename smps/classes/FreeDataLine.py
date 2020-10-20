from .DataLine import DataLine


class FreeDataLine(DataLine):

    def indicator(self) -> str:
        pass

    def first_header_word(self):
        pass

    def second_header_word(self):
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
