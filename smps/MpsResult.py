from pathlib import Path

from smps.parsers import MpsParser


class MpsResult:
    """
    Parsing result, containing all the data that was read from the MPS file.

    Arguments
    ---------
    mps : MpsParser
        MpsParser instance that was populated with the MPS data.
    """

    def __init__(self, mps: MpsParser):
        self._mps = mps

    @property
    def mps_location(self) -> Path:
        return self._mps.file_location()

    # TODO wrap around MpsParser
