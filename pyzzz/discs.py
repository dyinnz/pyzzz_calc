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
            source="Polar_Metal suit4 Ice DMG +20%+20%",
        ),
        DiscKind.Woodpecker_Electro: StaticBuff(
            StatValue(0.09 * 2, StatKind.ATK_RATIO),
            cov=1.0,
            source="Woodpecker_Electro suit4 ATK 9%+9%+9%",
        ),
        DiscKind.Swing_Jazz: StaticBuff(
            StatValue(0.15, StatKind.DMG_RATIO),
            # condition=HitContext(daze=True),
            source="Swing_Jazz suit4 DMG +15%",
            for_team=True,
        ),
        DiscKind.Fanged_Metal: StaticBuff(
            StatValue(0.35, StatKind.DMG_RATIO),
            source="Freedom_Blues suit4 DMG +35%",
        ),
    }

    return mapping.get(kind, None)
