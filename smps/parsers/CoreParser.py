from .MpsParser import MpsParser


class CoreParser(MpsParser):

    @property
    def _file_extensions(self):
        return [".cor", ".COR", ".core", ".CORE"]
