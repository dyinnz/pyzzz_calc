from pyzzz.buff import StaticBuff
from pyzzz.model import *


def get_suit4_buff(kind: DiscKind):
    mapping = {
        DiscKind.Polar_Metal: StaticBuff(
            StatValue(0.4, StatKind.DMG_RATIO),
            condition=[
                HitContext(atk_kind=AttackKind.Basic),
                HitContext(atk_kind=AttackKind.Dash),
            ],
            cov=0.8,
            owner="Polar_Metal",
            source="+20%/+20%",
        ),
        DiscKind.Woodpecker_Electro: StaticBuff(
            StatValue(0.09, StatKind.ATK_RATIO),
            cov=2.0,
            owner="Woodpecker_Electro",
            source="+9%/+9%/+9%",
        ),
        DiscKind.Swing_Jazz: StaticBuff(
            StatValue(0.15, StatKind.DMG_RATIO),
            owner="Swing_Jazz",
            for_team=True,
        ),
        DiscKind.Fanged_Metal: StaticBuff(
            StatValue(0.35, StatKind.DMG_RATIO),
            owner="Freedom_Blues",
        ),
    }

    return mapping.get(kind, None)
