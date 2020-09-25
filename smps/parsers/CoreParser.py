from .Parser import Parser


class CoreParser(Parser):
    FILE_EXTENSIONS = [".cor", ".COR", ".core", ".CORE"]

    def parse(self):
        pass
