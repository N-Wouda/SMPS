from .Parser import Parser


class TimeParser(Parser):
    FILE_EXTENSIONS = [".tim", ".TIM", ".time", ".TIME"]
    SECTIONS = ["TIME", "PERIODS", "ENDATA"]

    def _process_data_line(self, data_line):
        pass  # TODO
