from context import pyzzz

from pyzzz.model import StatKind, StatValue


def test_stat():
    kind = StatKind.DMG_RATIO
    assert "dmg_ratio" in str(kind)

