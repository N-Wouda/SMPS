import logging
import warnings
from pathlib import Path
from typing import Union

from smps.parsers import Parser, CoreParser, StochParser, TimeParser
from .SmpsResult import SmpsResult

logger = logging.getLogger(__name__)


def read_smps(*locations: Union[str, Path],
              is_fixed: bool = True) -> SmpsResult:
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
    is_fixed : bool, optional
        Type of file parsed. The SMPS files are either fixed width (True), or
        free form (False). Default True There are some nuances to this: see the
        second reference below for details.

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
    - Birge, J.R., Dempster, M.A.H., Gassmann, H.I., Gunn, E., King, A.J.,
      and Wallace, S.W. 1987. A Standard Input Format for Multiperiod Stochastic
      Linear Programs. `WP-87-118`.
      http://pure.iiasa.ac.at/id/eprint/2934/1/WP-87-118.pdf.
    - See http://lpsolve.sourceforge.net/5.5/mps-format.htm for a detailed
      description of the MPS format (CORE file), and http://tiny.cc/lsyxsz for
      a brief overview of various parts of the other SMPS file. Furthermore,
      we use Gassmann's extensive notes here: http://tiny.cc/b87ysz.
    """
    logger.debug(f"Parsing an SMPS triplet at locations {locations}.")

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

    if is_fixed:
        Parser.set_fixed()
    else:
        Parser.set_free()

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
