"""
Historically, the CoreParser came first. The MpsParser was split off only later.
As such, most tests are present in test_CoreParser.py, rather than this file.
"""

from numpy.testing import assert_warns

from smps.parsers import MpsParser


def test_ranges_warns_unknown_constraint():
    """
    This MPS file has an unknown constraint name in the RANGES data section. The
    implementation should warn about this.
    """
    parser = MpsParser("data/test/mps_unknown_constraint_ranges")

    with assert_warns(UserWarning):
        parser.parse()
