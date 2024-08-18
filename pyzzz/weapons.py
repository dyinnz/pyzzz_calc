import math
from typing import Sequence

from pyzzz import dataset
from pyzzz.buff import BuffBase, DynamicBuff
from pyzzz.model import *

CN2EN = {
    "加农转子": "CannonRotor",
    "街头巨星": "StarlightEngine",
}

EN2CN = {v: k for k, v in CN2EN.items()}


class Weapon:
    def __init__(self, name="", level=60, is_ascension=False, repetition=1):
        self._name = name

        # from dataset
        self._profession: Profession = Profession.All
        self._init: WeaponData = WeaponData(0, 0, StatValue.create_empty())
        self._growths: list[WeaponGrowth] = []
        self._ascensions: list[WeaponGrowth] = []

        # from input
        self._level = level
        self._is_ascension = is_ascension
        self._repetition = repetition

        self.data: WeaponData = WeaponData(level, 0, StatValue.create_empty())

        self._buffs: Sequence[BuffBase] = []

        if name:
            self.load_zzz_gg_data(name)
            self.fill_data()

    @property
    def level(self):
        return self._level

    def buffs(self, context: ContextData | None = None) -> Sequence[BuffBase]:
        return []

    def fill_data(self):
        self.data.level = self._level
        rank = (self._level - 1) // 10 + int(
            self._level % 10 == 0 and self._is_ascension
        )
        asc = self._ascensions[rank]
        self.data.atk = math.floor(
            self._init.atk * (1 + asc.atk_rate + self._growths[self._level].atk_rate)
        )
        self.data.primary.value = self._init.primary.value * (1 + asc.primary_rate)
        self.data.primary.kind = self._init.primary.kind

    def set_stats(self, level=None, is_ascension=None, repetition=None):
        if level is not None:
            self._level = level
        if is_ascension is not None:
            self._is_ascension = is_ascension
        if repetition is not None:
            self._repetition = repetition
        self.fill_data()

    def __str__(self):
        return f"{self._name} - {self._profession}\n{self._ascensions}\ninit: {self._init} - current: {self.data}"

    def load_zzz_gg_data(self, name: str):
        db = dataset.load_zzz_gg_weapons()

        weapon = db["weapons"][name]
        model = weapon["Rarity"]
        self._profession = Profession(weapon["ProfessionName"].lower())
        self._ascensions = db["ascensions"][model]
        self._growths = db["levelings"][model]

        self._init.atk = weapon["BaseProperty"]["Value"]
        self._init.primary.value = weapon["RandProperty"]["Value"]
        self._init.primary.kind = dataset.ZZZ_GG_STAT_PRIMARY[
            weapon["RandProperty"]["Name"]
        ]
        if "%" in weapon["RandProperty"]["ShowForm"]:
            self._init.primary.value /= 1e4


class CannonRotor(Weapon):
    NAME = "CannonRotor"

    def __init__(self, level=60, is_ascension=False, repetition=1):
        Weapon.__init__(self, CannonRotor.NAME, level, is_ascension, repetition)

    def buffs(self, context: ContextData | None = None):
        def create():
            return StatValue(
                [0, 0.075, 0.086, 0.097, 0.108, 0.120][self._repetition],
                StatKind.ATK_RATIO,
            )

        return [DynamicBuff(create, source="CannonRotor buff")]


class StarlightEngine(Weapon):
    NAME = "StarlightEngine"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        Weapon.__init__(self, StarlightEngine.NAME, level, is_ascension, repetition)
        self._cov = cov

    def buffs(self, context: ContextData | None = None):
        def create():
            return StatValue(
                [0, 0.12, 0.138, 0.156, 0.174, 0.192][self._repetition],
                StatKind.ATK_RATIO,
            )

        return [
            DynamicBuff(
                create,
                cov=self._cov,
                source="CannonRotor buff",
            )
        ]


class BashfulDemon(Weapon):
    NAME = "BashfulDemon"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        Weapon.__init__(self, BashfulDemon.NAME, level, is_ascension, repetition)
        self._cov = cov

    def buffs(self, context: ContextData | None = None):
        def create1():
            return StatValue(
                [0, 0.15, 0.175, 0.20, 0.22, 0.24][self._repetition], StatKind.DMG_RATIO
            )

        def create2():
            return StatValue(
                [0, 0.02, 0.023, 0.026, 0.029, 0.032][self._repetition],
                StatKind.ATK_RATIO,
            )

        return [
            DynamicBuff(
                create1,
                cov=self._cov,
                source="BashfulDemon buff 1",
            ),
            DynamicBuff(
                create2,
                cov=self._cov,
                source="BashfulDemon buff 2",
            ),
        ]


class PreciousFossilizedCore(Weapon):
    NAME = "PreciousFossilizedCore"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        Weapon.__init__(
            self, PreciousFossilizedCore.NAME, level, is_ascension, repetition
        )
        self._cov = cov


class DeepSeaVisitor(Weapon):
    NAME = "DeepSeaVisitor"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        Weapon.__init__(self, DeepSeaVisitor.NAME, level, is_ascension, repetition)
        self._cov = cov

    def buffs(self, context: ContextData | None = None):
        return [
            DynamicBuff(
                lambda: StatValue(
                    [0, 0.25, 0.315, 0.38, 0.445, 0.50][self._repetition],
                    StatKind.DMG_RATIO,
                ),
                cov=self._cov,
                source=f"{self._name} ice dmg buff",
            ),
            DynamicBuff(
                lambda: StatValue(
                    [0, 0.1, 0.125, 0.15, 0.175, 0.2][self._repetition],
                    StatKind.CRIT_RATIO,
                ),
                cov=self._cov,
                source=f"{self._name} ice crit ratio buff 1",
            ),
            DynamicBuff(
                lambda: StatValue(
                    [0, 0.1, 0.125, 0.15, 0.175, 0.2][self._repetition],
                    StatKind.CRIT_RATIO,
                ),
                cov=self._cov,
                source=f"{self._name} ice crit ratio buff 2",
            ),
        ]


def create_weapon(name: str, **kw):
    return {
        "CannonRotor": CannonRotor,
        "StarlightEngine": StarlightEngine,
        "BashfulDemon": BashfulDemon,
        "DeepSeaVisitor": DeepSeaVisitor,
        "PreciousFossilizedCore": PreciousFossilizedCore,
        "": Weapon
    }[name](**kw)
