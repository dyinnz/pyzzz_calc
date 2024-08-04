from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Optional

from pyzzz import util


class StatKind(StrEnum):
    STAT_EMPTY = auto()

    ATK_RATIO = auto()
    ATK_FLAT = auto()
    CRIT_RATIO = auto()
    CRIT_MULTI = auto()
    HP_RATIO = auto()
    HP_FLAT = auto()
    DEF_RATIO = auto()
    DEF_FLAT = auto()
    PEN_RATIO = auto()
    PEN_FLAT = auto()

    ANOMALY = auto()
    IMPACT = auto()
    ENERGY_REGEN = auto()

    DMG_RATIO = auto()  # TODO: support different DMG
    RES_RATIO = auto()
    STUN_DMG_RATIO = auto()


@dataclass
class StatValue:
    value: float
    kind: StatKind

    @staticmethod
    def empty():
        return StatValue(0, StatKind.STAT_EMPTY)

    def __bool__(self):
        return self.kind != StatKind.STAT_EMPTY

    def __repr__(self):
        if abs(self.value) > 1.0 or self.value == 0.0:
            return f"{self.kind}:{self.value:.3f}".rstrip("0").rstrip(".")
        else:
            return f"{self.kind}:{self.value * 100.0:.1f}%"

    def negative(self):
        return StatValue(-self.value, self.kind)

    @staticmethod
    def from_cn(name, value):
        if name in ("攻击力", "生命", "防御") and value[-1] == "%":
            name += "%"
        v = util.parse_float(value)
        kind = {
            "攻击力%": StatKind.ATK_RATIO,
            "攻击力": StatKind.ATK_FLAT,
            "暴击率": StatKind.CRIT_RATIO,
            "暴击伤害": StatKind.CRIT_RATIO,
            "生命值%": StatKind.HP_RATIO,
            "生命值": StatKind.HP_FLAT,
            "防御力%": StatKind.DEF_RATIO,
            "防御力": StatKind.DEF_FLAT,
            "穿透率": StatKind.PEN_RATIO,
            "穿透值": StatKind.PEN_FLAT,
            "异常精通": StatKind.ANOMALY,
            "冲击力": StatKind.IMPACT,
            "能量自动回复": StatKind.ENERGY_REGEN,
        }[name]
        return StatValue(v, kind)


class Attribute(StrEnum):
    All = auto()
    Physical = auto()
    Fire = auto()
    Ice = auto()
    Electric = auto()
    Ether = auto()


class AttackKind(StrEnum):
    All = auto()
    Basic = auto()
    Dodge = auto()  # 闪避反击
    Assit = auto()  # 支援攻击
    Special = auto()
    SpecialEx = auto()
    Chain = auto()
    Final = auto()


@dataclass
class Attack:
    kind: AttackKind = AttackKind.All
    attribute: Attribute = Attribute.All
    multi: float = 1.0


@dataclass
class AttackList:
    attacks: list

    def __iter__(self):
        return self.attacks.__iter__()

    def __next__(self):
        return self.__next__()


class DiscKind(StrEnum):
    Empty = auto()
    Summary = auto()

    # see https://zzz.hakush.in/equipment
    Fanged_Metal = auto()  # physical dmg
    Polar_Metal = auto()  # ice dmg
    Thunder_Metal = auto()  # electric dmg
    Chaotic_Metal = auto()  # ehter dmg
    Inferno_Metal = auto()  # fire dmg
    Swing_Jazz = auto()  # energy
    Soul_Rock = auto()  # def
    Hormone_Punk = auto()  # ATK%
    Freedom_Blues = auto()  # Anomaly Proficiency
    Shockstar_Disco = auto()  # impact
    Puffer_Electro = auto()  # pen
    Woodpecker_Electro = auto()  # crit

    def __repr__(self):
        return f"Disk.{self.name}"


@dataclass
class Disc:
    index: int
    kind: DiscKind
    primary: StatValue
    secondaries: list[StatValue] = field(default_factory=list)

    def empty(self):
        return self.primary.value == 0 and len(self.secondaries) == 0


@dataclass
class DiscGroup:
    @staticmethod
    def _default_discs():
        return [
            Disc(1, DiscKind.Empty, StatValue(0.0, StatKind.HP_FLAT)),
            Disc(2, DiscKind.Empty, StatValue(0.0, StatKind.ATK_FLAT)),
            Disc(3, DiscKind.Empty, StatValue(0.0, StatKind.DEF_FLAT)),
            Disc(4, DiscKind.Empty, StatValue(0.0, StatKind.CRIT_MULTI)),
            Disc(5, DiscKind.Empty, StatValue(0.0, StatKind.ATK_RATIO)),
            Disc(6, DiscKind.Empty, StatValue(0.0, StatKind.ATK_RATIO)),
        ]

    discs: list[Disc] = field(default_factory=_default_discs)
    suit2: list[DiscKind] = field(default_factory=list)
    suit2_stats: list[StatValue] = field(default_factory=list)
    suit4: DiscKind = DiscKind.Empty
    summary: Optional[Disc] = None

    def set(self, n, disc):
        self.discs[n - 1] = disc

    def at(self, n):
        return self.discs[n - 1]

    def make_suits(self):
        counts = {}
        for disc in self.discs:
            counts[disc.kind] = counts.get(disc.kind, 0) + 1
        self.suit2 = []
        for k, c in counts.items():
            if c >= 2:
                self.suit2.append(k)
            elif c >= 4:
                self.suit4 = k

    def make_summary(self, summary: Disc, suit2: list[DiscKind], suit4: DiscKind):
        self.summary = summary
        self.suit2 = [k for k in suit2 if str(k).endswith("metal")]
        self.suit4 = suit4

    def __repr__(self):
        s = "Discs:\n"
        if self.summary:
            s += f"\tSumary: {self.summary}\n"
        else:
            for disc in self.discs:
                if not disc.empty():
                    s += f"\t{disc}\n"
        if self.suit2_stats:
            s += "\tSuit2 stats:\t"
            for stat in self.suit2_stats:
                s += f"\t{stat}"
            s += "\n"
        s += "\tSuit2: ["
        s += ", ".join([str(k) for k in self.suit2])
        s += "]\t"
        s += f"Suit4: {self.suit4}"
        return s


@dataclass
class SkillLevels:
    core: int = 6  # NaN=0, A=1, F=6
    basic: int = 11
    dodge: int = 11
    special: int = 11
    chain: int = 11
    assit: int = 11


@dataclass
class SkillMutil:
    base: float = 1.0
    grow: float = 0.0


@dataclass
class AgentData:
    # NOTE: static data, buff not included here
    name: str = ""

    level: int = 0
    atk: float = 0.0
    crit_ratio: float = 0.05
    crit_multi: float = 0.50

    # not important
    hp: float = field(default=0.0, repr=False)
    defense: float = field(default=0.0, repr=False)
    impact: float = 0.0
    anomaiy_proficiency: float = 0.0
    attribte_master: float = 0.0
    energy_regen: float = field(default=0.0, repr=False)


@dataclass
class WeaponData:
    # NOTE: static data, buff not included here
    level: int
    atk: float
    primary: StatValue


@dataclass
class ContextData:
    # agent -> moster
    atk_attr: Optional[Attribute] = None
    atk_kind: Optional[AttackKind] = None
    assault: bool = False

    # moster
    daze: bool = False

    def contains(self, rhs):
        if (
            rhs.atk_attr
            and self.atk_attr != Attribute.All
            and self.atk_attr != rhs.atk_attr
        ):
            return False
        if (
            rhs.atk_kind
            and self.atk_kind != AttackKind.All
            and self.atk_kind != rhs.atk_kind
        ):
            return False
        if rhs.assault and not self.assault:
            return False
        if rhs.daze and not self.daze:
            return False
        return True
