from .Parser import Parser


class CoreParser(Parser):
    FILE_EXTENSIONS = [".cor", ".COR", ".core", ".CORE"]
    STEPS = {
        "NAME": lambda self, data_line: None,  # TODO
        "ROWS": lambda self, data_line: None,  # TODO
        "COLUMNS": lambda self, data_line: None,  # TODO
        "RHS": lambda self, data_line: None,  # TODO
        "BOUNDS": lambda self, data_line: None,  # TODO
        "RANGES": lambda self, data_line: None,  # TODO
    }
