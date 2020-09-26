from .Parser import Parser


class StochParser(Parser):
    FILE_EXTENSIONS = [".sto", ".STO", ".stoch", ".STOCH"]
    STEPS = {
        "STOCH": lambda self, data_line: None,  # TODO
        "INDEP": lambda self, data_line: None,  # TODO
        "BLOCKS": lambda self, data_line: None,  # TODO
        "SCENARIOS": lambda self, data_line: None,  # TODO
    }
