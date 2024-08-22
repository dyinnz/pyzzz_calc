import abc
import math
from dataclasses import dataclass, field
from enum import StrEnum, auto


class StatKind(StrEnum):
    STAT_EMPTY = auto()

    ATK_BASE = auto()
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
    DEF_RES = auto()

    ANOMALY_MASTER = auto()
    ANOMALY_PROFICIENCY = auto()
    IMPACT = auto()
    ENERGY_REGEN = auto()

    DMG_RATIO = auto()  # TODO: support different DMG
    RES_RATIO = auto()
    STUN_DMG_RATIO = auto()

    SKILL_MULTI = auto()


@dataclass
class StatValue:
    value: float
    kind: StatKind

    @staticmethod
    def create_empty():
        return StatValue(0, StatKind.STAT_EMPTY)

    def __bool__(self):
        return self.kind != StatKind.STAT_EMPTY

    def __repr__(self):
        if abs(self.value) > 1.0 or self.value == 0.0:
            return f"{self.kind}:{self.value:.3f}".rstrip("0").rstrip(".")
        else:
            return f"{self.kind}:{self.value * 100.0:.1f}%"

    def __sub__(self, rhs):
        if self.kind != rhs.kind:
            raise Exception(f"not same kind {self.kind} - {rhs.kind}")
        return StatValue(self.value - rhs.value, self.kind)

    def __add__(self, rhs):
        if self.kind != rhs.kind:
            raise Exception(f"not same kind {self.kind} - {rhs.kind}")
        return StatValue(self.value + rhs.value, self.kind)

    def __neg__(self):
        return StatValue(-self.value, self.kind)


class Attribute(StrEnum):
    All = auto()
    Physical = auto()
    Fire = auto()
    Ice = auto()
    Electric = auto()
    Ether = auto()


class AttackKind(StrEnum):
    All = auto()
    Anomaly = auto()
    Basic = auto()
    Dash = auto()
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
    anomaly: float = 0.0


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


def get_suit2_stat(kind: DiscKind) -> StatValue:
    mapping = {
        DiscKind.Fanged_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Polar_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Thunder_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Chaotic_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Inferno_Metal: StatValue(0.10, StatKind.DMG_RATIO),
        DiscKind.Hormone_Punk: StatValue(0.10, StatKind.ATK_RATIO),
        DiscKind.Puffer_Electro: StatValue(0.08, StatKind.PEN_RATIO),
        DiscKind.Woodpecker_Electro: StatValue(0.08, StatKind.CRIT_RATIO),
        DiscKind.Freedom_Blues: StatValue(30, StatKind.ANOMALY_PROFICIENCY),
    }

    return mapping.get(kind, StatValue.create_empty())


@dataclass
class Disc:
    index: int
    kind: DiscKind
    primary: StatValue
    secondaries: list[StatValue] = field(default_factory=list)

    def empty(self):
        return self.primary.value == 0 and self.kind == DiscKind.Empty


@dataclass
class DiscGroup:
    @staticmethod
    def _default_discs():
        return [
            Disc(1, DiscKind.Empty, StatValue(2200, StatKind.HP_FLAT)),
            Disc(2, DiscKind.Empty, StatValue(316, StatKind.ATK_FLAT)),
            Disc(3, DiscKind.Empty, StatValue(184, StatKind.DEF_FLAT)),
            Disc(4, DiscKind.Empty, StatValue(24, StatKind.CRIT_RATIO)),
            Disc(5, DiscKind.Empty, StatValue(30, StatKind.DMG_RATIO)),
            Disc(6, DiscKind.Empty, StatValue(30, StatKind.ATK_RATIO)),
        ]

    discs: list[Disc] = field(default_factory=_default_discs)
    suit2: list[DiscKind] = field(default_factory=list)
    suit2_stats: list[StatValue] = field(default_factory=list)
    suit4: DiscKind = DiscKind.Empty
    summary: Disc | None = None

    def set(self, disc: Disc):
        self.discs[disc.index - 1] = disc

    def at(self, n):
        return self.discs[n - 1]

    def generate_suits(self):
        counts = {}
        for disc in self.discs:
            counts[disc.kind] = counts.get(disc.kind, 0) + 1
        self.suit2 = []
        sorted_item = sorted(counts.items(), key=lambda t: t[1])
        for k, c in sorted_item:
            if c >= 2:
                self.suit2.append(k)
            if c >= 4:
                self.suit4 = k
        self.suit2_stats = [get_suit2_stat(k) for k in self.suit2]

    def make_summary(
        self, summary: Disc, suit2: list[DiscKind], suit4: DiscKind | None
    ):
        self.summary = summary
        self.suit2 = [k for k in suit2 if str(k).endswith("metal")]
        self.suit4 = suit4 if suit4 else DiscKind.Empty
        self.suit2_stats = [get_suit2_stat(k) for k in self.suit2]

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
    assit: int = 11
    dodge: int = 11  # dash + dodge
    special: int = 11
    chain: int = 11  # chain + final

    def __post_init__(self):
        self.core = min(6, self.core)
        self.basic = min(16, self.basic)
        self.dodge = min(16, self.dodge)
        self.assit = min(16, self.assit)
        self.special = min(16, self.special)
        self.chain = min(16, self.chain)

    @property
    def dash(self):
        return self.dodge

    @property
    def final(self):
        return self.chain


@dataclass
class SkillMutil:
    base: float = 1.0
    grow: float = 0.0
    anomaly: float = 0.0


class Profession(StrEnum):
    All = auto()
    Attack = auto()
    Stun = auto()
    Anomaly = auto()
    Support = auto()
    Defense = auto()


class Camp(StrEnum):
    Unknown = auto()
    Cunning_Hares = auto()
    Obol_Squad = auto()
    Victoria_Housekeeping = auto()
    Belobog_Heavy_Industries = auto()
    Section_6 = auto()
    Sons_of_Calydon = auto()
    Public_Security = auto() 
    Criminal_Investigation_Special_Response_Team = auto()

    @staticmethod
    def from_full_name(name: str):
        return {
            "Belobog Heavy Industries": Camp.Belobog_Heavy_Industries,
            "Cunning Hares": Camp.Cunning_Hares,
            "Hollow Special Operations Section 6": Camp.Section_6,
            "New Eridu Public Security": Camp.Public_Security,
            "Obol Squad": Camp.Obol_Squad,
            "Sons of Calydon": Camp.Sons_of_Calydon,
            "Victoria Housekeeping Co.": Camp.Victoria_Housekeeping,
            "Criminal Investigation Special Response Team": Camp.Criminal_Investigation_Special_Response_Team,
        }[name]


@dataclass
class AgentData:
    # NOTE: static data, buff not included here
    level: int = 0

    atk_base: float = 0.0
    atk_weapon: float = 0.0
    atk_flat: float = 0.0
    atk_ratio: float = 0.0
    crit_ratio: float = 0.05
    crit_multi: float = 0.50

    # not important
    hp: float = field(default=0.0, repr=False)
    defense: float = field(default=0.0, repr=False)
    impact: float = 0.0
    anomaly_master: float = 0.0
    anomaly_proficiency: float = 0.0
    energy_regen: float = field(default=0.0, repr=False)

    pen_ratio: float = 0.0
    pen_flat: float = 0.0
    dmg_ratio: float = 0.0

    def static_atk(self):
        return math.floor(
            (self.atk_base + self.atk_weapon) * (1.0 + self.atk_ratio) + self.atk_flat
        )

    def apply_stat(self, stat: StatValue):
        if stat.kind == StatKind.STAT_EMPTY:
            pass
        elif stat.kind == StatKind.ATK_BASE:
            self.atk_base += stat.value
        elif stat.kind == StatKind.ATK_RATIO:
            self.atk_ratio += stat.value
        elif stat.kind == StatKind.ATK_FLAT:
            self.atk_flat += stat.value
        elif stat.kind == StatKind.CRIT_RATIO:
            self.crit_ratio += stat.value
        elif stat.kind == StatKind.CRIT_MULTI:
            self.crit_multi += stat.value
        elif stat.kind == StatKind.PEN_RATIO:
            self.pen_ratio += stat.value
        elif stat.kind == StatKind.PEN_FLAT:
            self.pen_flat += stat.value
        elif stat.kind == StatKind.DMG_RATIO:
            self.dmg_ratio += stat.value

        elif stat.kind == StatKind.HP_FLAT:
            self.hp += stat.value
        elif stat.kind == StatKind.DEF_FLAT:
            self.defense += stat.value
        elif stat.kind == StatKind.IMPACT:
            self.impact += stat.value
        elif stat.kind == StatKind.ENERGY_REGEN:
            self.energy_regen += stat.value
        elif stat.kind == StatKind.ANOMALY_MASTER:
            self.anomaly_master += stat.value
        elif stat.kind == StatKind.ANOMALY_PROFICIENCY:
            self.anomaly_proficiency += stat.value
        else:
            raise Exception(f"not supported stat kind {stat.kind} for agent data")

    def __sub__(self, rhs):
        return AgentData(
            self.level - rhs.level,
            self.atk_base - rhs.atk_base,
            self.atk_weapon - rhs.atk_weapon,
            self.atk_flat - rhs.atk_flat,
            self.atk_ratio - rhs.atk_ratio,
            self.crit_ratio - rhs.crit_ratio,
            self.crit_multi - rhs.crit_multi,
            self.hp - rhs.hp,
            self.defense - rhs.defense,
            self.impact - rhs.impact,
            self.anomaly_proficiency - rhs.anomaiy_proficiency,
            self.anomaly_master - rhs.attribte_master,
            self.energy_regen - rhs.energy_regen,
            self.pen_ratio - rhs.pen_ratio,
            self.pen_flat - rhs.pen_flat,
            self.dmg_ratio - rhs.dmg_ratio,
        )

    def __add__(self, rhs):
        return AgentData(
            self.level + rhs.level,
            self.atk_base + rhs.atk_base,
            self.atk_weapon + rhs.atk_weapon,
            self.atk_flat + rhs.atk_flat,
            self.atk_ratio + rhs.atk_ratio,
            self.crit_ratio + rhs.crit_ratio,
            self.crit_multi + rhs.crit_multi,
            self.hp + rhs.hp,
            self.defense + rhs.defense,
            self.impact + rhs.impact,
            self.anomaly_proficiency + rhs.anomaiy_proficiency,
            self.anomaly_master + rhs.attribte_master,
            self.energy_regen + rhs.energy_regen,
            self.pen_ratio + rhs.pen_ratio,
            self.pen_flat + rhs.pen_flat,
            self.dmg_ratio + rhs.dmg_ratio,
        )


@dataclass
class AgentDataWithGrowth:
    init: AgentData = field(default_factory=AgentData)
    atk_growth: float = 0.0
    hp_growth: float = 0.0
    defense_growth: float = 0.0


@dataclass
class WeaponGrowth:
    atk_rate: float = 0.0
    primary_rate: float = 0.0


@dataclass
class ContextData:
    agent: str = ""  # empty str means that wound apply to all the agents

    # agent -> moster
    atk_attr: Attribute | None = None
    atk_kind: AttackKind | None = None
    assault: bool = False

    # moster
    daze: bool = False

    def contains(self, rhs):
        if rhs.agent and self.agent and self.agent != rhs.agent:
            return False
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


class ExtraMultiplier:
    @abc.abstractmethod
    def calc(self) -> float:
        pass

    @abc.abstractmethod
    def active(self, anomaly: bool, context: ContextData) -> bool:
        pass

    @abc.abstractmethod
    def show(self) -> str:
        pass
