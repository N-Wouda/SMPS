from .Parser import Parser


class StochParser(Parser):
    FILE_EXTENSIONS = [".sto", ".STO", ".stoch", ".STOCH"]
    SECTIONS = ["STOCH", "INDEP", "BLOCKS", "SCENARIOS", "ENDATA"]

    def parse(self):
        for line in self._line():
            pass  # TODO
