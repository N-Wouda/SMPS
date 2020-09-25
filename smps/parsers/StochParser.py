from .Parser import Parser


class StochParser(Parser):
    FILE_EXTENSIONS = [".sto", ".STO", ".stoch", ".STOCH"]
    SECTIONS = ["STOCH", "INDEP", "BLOCKS", "SCENARIOS", "ENDATA"]

    def _process_data_line(self, data_line):
        pass  # TODO
