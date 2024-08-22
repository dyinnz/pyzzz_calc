from pyzzz import dataset
from pyzzz.buff import DynamicBuff
from pyzzz.model import Profession, StatKind, StatValue, ContextData
from pyzzz.weapon import Weapon

CN2EN = {
    "加农转子": "CannonRotor",
    "街头巨星": "StarlightEngine",
}

EN2CN = {v: k for k, v in CN2EN.items()}


class WeaponWithData(Weapon):
    def __init__(
        self,
        name: str = "",
        level: int = 60,
        is_ascension: bool = False,
        repetition: int = 1,
    ):
        super().__init__(name, level, is_ascension, repetition)
        if name:
            self._load_zzz_gg_data(name)

    def _load_zzz_gg_data(self, name: str):
        db = dataset.load_zzz_gg_weapons()

        weapon = db["weapons"][name]
        model = weapon["Rarity"]
        self._profession = Profession(weapon["ProfessionName"].lower())
        self._ascensions = db["ascensions"][model]
        self._growths = db["levelings"][model]

        self._init_atk_base = weapon["BaseProperty"]["Value"]
        self._init_advanced_stat.value = weapon["RandProperty"]["Value"]
        self._init_advanced_stat.kind = dataset.ZZZ_GG_STAT_PRIMARY[
            weapon["RandProperty"]["Name"]
        ]
        if "%" in weapon["RandProperty"]["ShowForm"]:
            self._init_advanced_stat.value /= 1e4

        self._fill_data()


class CannonRotor(WeaponWithData):
    NAME = "CannonRotor"

    def __init__(self, level=60, is_ascension=False, repetition=1):
        super().__init__(CannonRotor.NAME, level, is_ascension, repetition)

    def buffs(self, context: ContextData | None = None):
        def create():
            return StatValue(
                [0, 0.075, 0.086, 0.097, 0.108, 0.120][self._repetition],
                StatKind.ATK_RATIO,
            )

        return [DynamicBuff(create, source="CannonRotor buff")]


class StarlightEngine(WeaponWithData):
    NAME = "StarlightEngine"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        super().__init__(StarlightEngine.NAME, level, is_ascension, repetition)
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


class BashfulDemon(WeaponWithData):
    NAME = "BashfulDemon"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        super().__init__(BashfulDemon.NAME, level, is_ascension, repetition)
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


class PreciousFossilizedCore(WeaponWithData):
    NAME = "PreciousFossilizedCore"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        Weapon.__init__(
            self, PreciousFossilizedCore.NAME, level, is_ascension, repetition
        )
        self._cov = cov


class DeepSeaVisitor(WeaponWithData):
    NAME = "DeepSeaVisitor"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        super().__init__(DeepSeaVisitor.NAME, level, is_ascension, repetition)
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


class RainforestGourmet(WeaponWithData):
    NAME = "RainforestGourmet"

    def __init__(self, cov=1.0, level=60, is_ascension=False, repetition=1):
        super().__init__(RainforestGourmet.NAME, level, is_ascension, repetition)
        self._cov = cov


def create_weapon(name: str, **kw):
    name = name.replace(" ", "")
    mappings = {
        "CannonRotor": CannonRotor,
        "StarlightEngine": StarlightEngine,
        "BashfulDemon": BashfulDemon,
        "DeepSeaVisitor": DeepSeaVisitor,
        "PreciousFossilizedCore": PreciousFossilizedCore,
        "RainforestGourmet": RainforestGourmet,
    }
    if name in mappings:
        return mappings[name](**kw)
    elif name:
        return Weapon(name, **kw)
