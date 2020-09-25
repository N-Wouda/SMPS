from .Parser import Parser


class CoreParser(Parser):
    FILE_EXTENSIONS = [".cor", ".COR", ".core", ".CORE"]
    SECTIONS = ["NAME", "ROWS", "COLUMNS", "RHS", "BOUNDS", "RANGES", "ENDATA"]

    def parse(self):
        for line in self._line():
            pass  # TODO
