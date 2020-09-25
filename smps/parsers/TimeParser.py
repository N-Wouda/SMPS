from .Parser import Parser


class TimeParser(Parser):
    FILE_EXTENSIONS = [".tim", ".TIM", ".time", ".TIME"]
    SECTIONS = ["TIME", "PERIODS", "ENDATA"]

    def parse(self):
        for line in self._line():
            pass  # TODO
