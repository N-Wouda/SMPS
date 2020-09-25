from .Parser import Parser


class CoreParser(Parser):
    FILE_EXTENSIONS = [".cor", ".COR", ".core", ".CORE"]
    SECTIONS = ["NAME", "ROWS", "COLUMNS", "RHS", "BOUNDS", "RANGES", "ENDATA"]

    def _process_data_line(self, data_line):
        pass  # TODO

