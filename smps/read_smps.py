import logging
import warnings
from pathlib import Path
from typing import Union

from smps.SmpsResult import SmpsResult
from smps.parsers import CoreParser, StochParser, TimeParser

logger = logging.getLogger(__name__)


def smps(*locations: Union[str, Path]) -> SmpsResult:
    """
    Parses a triplet of SMPS files.

    Parameters
    ----------
    *locations : Union[str, Path]
        File-system location(s) of the SMPS triplet of files. If only a single
        string is passed, it is assumed this identifies all three files (with
        extensions .cor or .core for the CORE file, .tim or .time for the
        TIME file, and .sto or .stoch for the STOCH file). If (more than) three
        locations are passed, it is assumed the first identifies the CORE file,
        the second the TIME file, and the third the STOCH file. Any remaining
        arguments are ignored.

    Returns
    -------
    SmpsResult
        An object equipped with all the parsed SMPS data, and several methods
        for processing it.

    Raises
    ------
    FileNotFoundError
        When one of the CORE, TIME, or STOCH files does not exist.
    ValueError
        When a number of locations other than 1 or 3(+) is received.

    References
    ----------
    See http://lpsolve.sourceforge.net/5.5/mps-format.htm for a detailed
    description of the MPS format (CORE file), and http://tiny.cc/lsyxsz for
    a brief overview of various parts of the other SMPS file.
    """
    logger.debug(f"Creating an SMPS instance with arguments {locations}.")

    if len(locations) == 1:
        location = Path(locations[0])

        core_location = location
        time_location = location
        stoch_location = location
    elif len(locations) >= 3:
        core_location = Path(locations[0])
        time_location = Path(locations[1])
        stoch_location = Path(locations[2])
    else:
        msg = f"Received {len(locations)} locations, expected 1 or 3."
        logger.error(msg)
        raise ValueError(msg)

    core = CoreParser(core_location)
    core.parse()

    time = TimeParser(time_location)
    time.parse()

    stoch = StochParser(stoch_location)
    stoch.parse()

    if len({core.name, time.name, stoch.name}) != 1:
        msg = "The names in the CORE, TIME, and STOCH files do not agree."
        logger.warning(msg)
        warnings.warn(msg)

    return SmpsResult(core, time, stoch)
