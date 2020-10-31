import logging
from pathlib import Path
from typing import Union

from smps.parsers import MpsParser
from .MpsResult import MpsResult

logger = logging.getLogger(__name__)


def read_mps(location: Union[str, Path]) -> MpsResult:
    """
    Parses an MPS file.

    Parameters
    ----------
    location : Union[str, Path]
        File-system location(s) of the MPS file to parse.

    Returns
    -------
    MpsResult
        An object equipped with all the parsed MPS data, and several methods
        for processing it.

    Raises
    ------
    FileNotFoundError
        When the MPS file does not exist.

    References
    ----------
    - See http://lpsolve.sourceforge.net/5.5/mps-format.htm for a detailed
      description of the MPS format (CORE file), and http://tiny.cc/lsyxsz for
      a brief overview of various parts of the other SMPS file. Furthermore,
      we use Gassmann's extensive notes here: http://tiny.cc/b87ysz.
    """
    logger.debug(f"Parsing MPS file at {location}")

    mps = MpsParser(location)
    mps.parse()

    return MpsResult(mps)
