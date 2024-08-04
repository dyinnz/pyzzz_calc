from pyzzz.buff import Buff
from pyzzz.model import *


def get_suit2_stat(kind: DiscKind):

    mapping = {
        DiscKind.Fanged_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Polar_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Thunder_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Chaotic_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Inferno_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Hormone_Punk: StatValue(0.10, StatKind.ATK_RATIO),
        DiscKind.Puffer_Electro: StatValue(0.08, StatKind.PEN_RATIO),
        DiscKind.Woodpecker_Electro: StatValue(0.08, StatKind.CRIT_RATIO),
    }

    return mapping.get(kind, None)


def get_suit4_buff(kind: DiscKind):

    mapping = {
        DiscKind.Polar_Metal: Buff(
            StatValue(0.4, StatKind.DMG_RATIO),
            cov=0.8,
            source="Polar_Metal suit4 Ice DMG +20%+20%",
        ),
        DiscKind.Swing_Jazz: Buff(
            StatValue(0.15, StatKind.DMG_RATIO),
            condition=ContextData(daze=True),
            source="Swing_Jazz suit4 DMG +15%",
        ),
    }

    return mapping.get(kind, None)
