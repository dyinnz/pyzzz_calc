from context import pyzzz

from pyzzz.model import StatKind, StatValue


def test_stat():
    kind = StatKind.DMG_PERCENT
    assert "DMG_PERCENT" in str(kind)

