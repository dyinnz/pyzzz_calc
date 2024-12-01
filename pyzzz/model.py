import typing as t
import copy
import abc
from dataclasses import dataclass, field
from enum import StrEnum, auto
from pydantic import BaseModel


class StatKind(StrEnum):
    EMPTY = auto()

    ATK_BASE = auto()
    ATK_RATIO = auto()
    ATK_FLAT = auto()
    HP_BASE = auto()
    HP_RATIO = auto()
    HP_FLAT = auto()
    DEF_BASE = auto()
    DEF_RATIO = auto()
    DEF_FLAT = auto()
    IMPACT = auto()
    IMPACT_RATIO = auto()
    ENERGY_REGEN = auto()
    ENERGY_REGEN_RATIO = auto()
    ANOMALY_MASTER = auto()
    ANOMALY_MASTER_RATIO = auto()

    CRIT_RATIO = auto()
    CRIT_MULTI = auto()
    PEN_RATIO = auto()
    PEN_FLAT = auto()
    ANOMALY_PROFICIENCY = auto()
    ACC_RATIO = auto()

    DMG_RATIO = auto()
    DMG_RATIO_PHYSICAL = auto()
    DMG_RATIO_FIRE = auto()
    DMG_RATIO_ICE = auto()
    DMG_RATIO_ELECTRIC = auto()
    DMG_RATIO_EHTER = auto()

    # on enemy
    ATTR_RES = auto()
    ANOMALY_RES = auto()
    STUN_DMG_RATIO = auto()
    DEF_REDUCE = auto()

    SKILL_MULTI = auto()

    def is_pct(self):
        return "ratio" in self or "multi" in self

    def __str__(self):
        return {
            StatKind.EMPTY: "EMPTY",
            StatKind.ATK_BASE: "ATK_BASE",
            StatKind.ATK_RATIO: "ATK",
            StatKind.ATK_FLAT: "ATK",
            StatKind.HP_BASE: "HP",
            StatKind.HP_RATIO: "HP",
            StatKind.HP_FLAT: "HP",
            StatKind.DEF_BASE: "DEF",
            StatKind.DEF_RATIO: "DEF",
            StatKind.DEF_FLAT: "DEF",
            StatKind.IMPACT: "IMPACT",
            StatKind.IMPACT_RATIO: "IMPACT",
            StatKind.ENERGY_REGEN: "ENERGY_REGEN",
            StatKind.ENERGY_REGEN_RATIO: "ENERGY_REGEN",
            StatKind.ANOMALY_MASTER: "AM",
            StatKind.ANOMALY_MASTER_RATIO: "AM",
            StatKind.CRIT_RATIO: "CRIT_RATIO",
            StatKind.CRIT_MULTI: "CRIT_MULTI",
            StatKind.PEN_RATIO: "PEN_RATIO",
            StatKind.PEN_FLAT: "PEN_FLAT",
            StatKind.ANOMALY_PROFICIENCY: "AP",
            StatKind.ACC_RATIO: "ACC_RATIO",
            StatKind.DMG_RATIO: "DMG",
            StatKind.DMG_RATIO_PHYSICAL: "PHYSICAL",
            StatKind.DMG_RATIO_FIRE: "FIRE",
            StatKind.DMG_RATIO_ICE: "ICE",
            StatKind.DMG_RATIO_ELECTRIC: "ELECTRIC",
            StatKind.DMG_RATIO_EHTER: "EHTER",
            StatKind.ATTR_RES: "RESISTANCE",
            StatKind.ANOMALY_RES: "ANOMALY_RES",
            StatKind.STUN_DMG_RATIO: "STUN_DMG",
            StatKind.DEF_REDUCE: "DEF_REDUCE",
            StatKind.SKILL_MULTI: "SKILL",
        }[self]

    def with_pct(self):
        return f"{self}" + ("%" if self.is_pct() else "")


@dataclass
class StatValue:
    value: float
    kind: StatKind

    @staticmethod
    def create_empty():
        return StatValue(0, StatKind.EMPTY)

    def __bool__(self):
        return self.kind != StatKind.EMPTY

    def __repr__(self):
        sign = "+" if self.value >= 0.0 else "-"
        if self.kind.is_pct():
            s = f"{self.kind} {sign}{abs(self.value) * 100.0:.1f}"
            return s.rstrip("0").rstrip(".") + "%"
        else:
            return f"{self.kind} {sign}{abs(self.value):.3f}".rstrip("0").rstrip(".")

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
    All = "All"
    Anomaly = "Anomaly"
    Basic = "Basic"
    Dash = "Dash"
    Dodge = "Dodge"  # 闪避反击
    QuickAssit = "QuickAssit"  # 快速支援
    DefenseAssit = "DefenseAssit"  # 招架支援
    Assit = "Assit"  # 支援突击
    Special = "Special"
    SpecialEx = "SpecialEx"
    Chain = "Chain"
    Final = "Final"


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
    Chaos_Jazz = auto()  # Anomaly Proficiency
    Shockstar_Disco = auto()  # impact
    Puffer_Electro = auto()  # pen
    Woodpecker_Electro = auto()  # crit

    def __repr__(self):
        return f"Disk.{self.name}"


def get_suit2_stat(kind: DiscKind) -> StatValue:
    mapping = {
        DiscKind.Fanged_Metal: StatValue(0.10, StatKind.DMG_RATIO_PHYSICAL),
        DiscKind.Polar_Metal: StatValue(0.10, StatKind.DMG_RATIO_ICE),
        DiscKind.Thunder_Metal: StatValue(0.10, StatKind.DMG_RATIO_ELECTRIC),
        DiscKind.Chaotic_Metal: StatValue(0.10, StatKind.DMG_RATIO_EHTER),
        DiscKind.Inferno_Metal: StatValue(0.10, StatKind.DMG_RATIO_FIRE),
        DiscKind.Hormone_Punk: StatValue(0.10, StatKind.ATK_RATIO),
        DiscKind.Puffer_Electro: StatValue(0.08, StatKind.PEN_RATIO),
        DiscKind.Woodpecker_Electro: StatValue(0.08, StatKind.CRIT_RATIO),
        DiscKind.Freedom_Blues: StatValue(30, StatKind.ANOMALY_PROFICIENCY),
        DiscKind.Swing_Jazz: StatValue(0.20, StatKind.ENERGY_REGEN_RATIO),
        DiscKind.Chaos_Jazz: StatValue(30, StatKind.ANOMALY_PROFICIENCY),
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

    def __str__(self):
        head = f"#{self.index} {self.kind:<20}{self.primary}"
        s = f"{head: <40}"
        s += "[ "
        s += " / ".join((str(s) for s in self.secondaries))
        s += " ]"
        return s

    def set_index(self, i: int):
        self.index = i
        return self

    def set_kind(self, k: DiscKind):
        self.kind = k
        return self

    def set_stats(self, p: StatValue, s: list[StatValue]):
        self.primary = p
        self.secondaries = s
        return self


@dataclass
class DiscGroup:
    @staticmethod
    def _default_discs():
        return [
            Disc(1, DiscKind.Empty, StatValue(2200, StatKind.HP_FLAT)),
            Disc(2, DiscKind.Empty, StatValue(316, StatKind.ATK_FLAT)),
            Disc(3, DiscKind.Empty, StatValue(184, StatKind.DEF_FLAT)),
            Disc(4, DiscKind.Empty, StatValue(0.24, StatKind.CRIT_RATIO)),
            Disc(5, DiscKind.Empty, StatValue(0.30, StatKind.DMG_RATIO)),
            Disc(6, DiscKind.Empty, StatValue(0.30, StatKind.ATK_RATIO)),
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
            s += "\tSuit2 Stats:"
            for stat in self.suit2_stats:
                s += f"\t{stat}"
            s += "\t"
        s += " Suits #2 ["
        s += ", ".join([str(k) for k in self.suit2])
        s += "] "
        s += f"#4 {self.suit4}"
        return s


@dataclass
class SkillLevels:
    core: int = 6  # NaN=0, A=1, F=6
    basic: int = 11
    dodge: int = 11  # dash + dodge
    assit: int = 11
    special: int = 11
    chain: int = 11  # chain + final

    def get(self, kind: AttackKind) -> int:
        if kind == AttackKind.Basic:
            return self.basic
        elif kind == AttackKind.Dash or kind == AttackKind.Dodge:
            return self.dodge
        elif (
            kind == AttackKind.DefenseAssit
            or kind == AttackKind.QuickAssit
            or kind == AttackKind.Assit
        ):
            return self.assit
        elif kind == AttackKind.Special or kind == AttackKind.SpecialEx:
            return self.special
        elif kind == AttackKind.Chain or kind == AttackKind.Final:
            return self.chain

        return 1

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
    Criminal_Investigation = auto()

    @staticmethod
    def from_full_name(name: str):
        return {
            "Belobog Heavy Industries": Camp.Belobog_Heavy_Industries,
            "Cunning Hares": Camp.Cunning_Hares,
            "Hollow Special Operations Section 6": Camp.Section_6,
            "Obol Squad": Camp.Obol_Squad,
            "Sons of Calydon": Camp.Sons_of_Calydon,
            "Victoria Housekeeping Co.": Camp.Victoria_Housekeeping,
            "Criminal Investigation Special Response Team": Camp.Criminal_Investigation,
        }[name]


@dataclass
class AgentRatioStats:
    # TYPE-1 :  (init + base) * (1 + ratio) + flat
    atk: float = 0.0
    hp: float = 0.0
    defense: float = 0.0
    impact: float = 0.0
    energy_regen: float = 0.0
    anomaly_master: float = 0.0


@dataclass
class AgentValueStats:
    # base = init + init * grow
    #           (          static         )   (    dynamic     )
    # TYPE-1 :  (base * (1 + ratio) + flat) * (1 + ratio) + flat
    atk: float = 0.0
    hp: float = 0.0
    defense: float = 0.0
    impact: float = 0.0
    energy_regen: float = 0.0
    anomaly_master: float = 0.0

    # TYPE-2 :  base + delta
    crit_ratio: float = 0.0
    crit_multi: float = 0.0

    anomaly_proficiency: float = 0.0
    acc_ratio: float = 0.0
    pen_ratio: float = 0.0
    pen_flat: float = 0.0

    dmg_ratio: float = 0.0
    dmg_ratio_physical: float = 0.0
    dmg_ratio_fire: float = 0.0
    dmg_ratio_electric: float = 0.0
    dmg_ratio_ice: float = 0.0
    dmg_ratio_ether: float = 0.0

    def dmg_ratio_attrs(self):
        return {
            StatKind.DMG_RATIO_PHYSICAL: self.dmg_ratio_physical,
            StatKind.DMG_RATIO_FIRE: self.dmg_ratio_fire,
            StatKind.DMG_RATIO_ELECTRIC: self.dmg_ratio_electric,
            StatKind.DMG_RATIO_ICE: self.dmg_ratio_ice,
            StatKind.DMG_RATIO_EHTER: self.dmg_ratio_ether,
        }

    def calc_dmg_ratio(self, kind: Attribute) -> float:
        result = self.dmg_ratio
        if kind == Attribute.Physical:
            result += self.dmg_ratio_physical
        elif kind == Attribute.Fire:
            result += self.dmg_ratio_fire
        elif kind == Attribute.Electric:
            result += self.dmg_ratio_electric
        elif kind == Attribute.Ice:
            result += self.dmg_ratio_ice
        elif kind == Attribute.Ether:
            result += self.dmg_ratio_ether
        return result

    def apply_ratio_delta(self, ratio: AgentRatioStats, delta: t.Self):
        for attr, value in ratio.__dict__.items():
            self.__dict__[attr] *= 1 + value

        for attr, value in delta.__dict__.items():
            self.__dict__[attr] += value

    def apply_base_stat(self, stat: StatValue) -> bool:
        if stat.kind == StatKind.ATK_BASE:
            self.atk += stat.value
        elif stat.kind == StatKind.HP_BASE:
            self.hp += stat.value
        elif stat.kind == StatKind.DEF_BASE:
            self.defense += stat.value
        elif stat.kind == StatKind.IMPACT:
            self.impact += stat.value
        elif stat.kind == StatKind.ENERGY_REGEN:
            self.energy_regen += stat.value
        elif stat.kind == StatKind.ANOMALY_MASTER:
            self.anomaly_master += stat.value
        else:
            return False
        return True

    def __str__(self):
        s = ""
        s += f"> ATK  {self.atk:<8}\tCRIT {self.crit_ratio * 100:.1f}% x {self.crit_multi * 100:.1f}%\t"
        s += f"\tDMG  {self.dmg_ratio * 100:.1f}%"
        for k, d in self.dmg_ratio_attrs().items():
            if d > 0:
                kind = k[len(StatKind.DMG_RATIO) + 1 :].upper()
                s += f"\t{kind} {d * 100:.1f}%"
        s += "\n"
        s += f"> HP   {self.hp:<8}\tDEF  {self.defense:<8}\tIMPACT {self.impact:<8}\tENERGY_REGEN {self.energy_regen:<8}\n"
        s += f"> AM   {self.anomaly_master:<8}\tAP   {self.anomaly_proficiency:<8}\tPEN_RATIO {self.pen_ratio * 100:.1f}%\tPEN_FLAT {self.pen_flat}\n"
        return s


AgentBaseStats = AgentValueStats
AgentFlatStats = AgentValueStats


@dataclass
class AgentGrowthStats:
    zero: AgentValueStats = field(default_factory=AgentValueStats)
    atk_growth: float = 0.0
    hp_growth: float = 0.0
    defense_growth: float = 0.0


@dataclass
class AgentStats:
    base: AgentBaseStats = field(default_factory=AgentBaseStats)
    ratio: AgentRatioStats = field(default_factory=AgentRatioStats)
    flat: AgentFlatStats = field(default_factory=AgentFlatStats)

    def calc_ap(self):
        return self.base.anomaly_proficiency + self.flat.anomaly_proficiency

    def calc_final(self, weapon_atk=0.0):
        result = AgentStats()
        result.base = copy.deepcopy(self.base)
        result.base.atk += weapon_atk
        result.base.apply_ratio_delta(self.ratio, self.flat)
        return result

    def apply_stat(self, stat: StatValue):
        if stat.kind == StatKind.EMPTY:
            pass
        elif stat.kind == StatKind.ATK_BASE:
            self.base.atk += stat.value
        elif stat.kind == StatKind.ATK_RATIO:
            self.ratio.atk += stat.value
        elif stat.kind == StatKind.ATK_FLAT:
            self.flat.atk += stat.value
        elif stat.kind == StatKind.HP_BASE:
            self.base.hp += stat.value
        elif stat.kind == StatKind.HP_RATIO:
            self.ratio.hp += stat.value
        elif stat.kind == StatKind.HP_FLAT:
            self.flat.hp += stat.value
        elif stat.kind == StatKind.DEF_BASE:
            self.base.defense += stat.value
        elif stat.kind == StatKind.DEF_RATIO:
            self.ratio.defense += stat.value
        elif stat.kind == StatKind.DEF_FLAT:
            self.flat.defense += stat.value
        elif stat.kind == StatKind.IMPACT:
            self.base.impact += stat.value
        elif stat.kind == StatKind.IMPACT_RATIO:
            self.ratio.impact += stat.value
        elif stat.kind == StatKind.ENERGY_REGEN:
            self.base.energy_regen += stat.value
        elif stat.kind == StatKind.ENERGY_REGEN_RATIO:
            self.ratio.energy_regen += stat.value
        elif stat.kind == StatKind.ANOMALY_MASTER:
            self.base.anomaly_master += stat.value
        elif stat.kind == StatKind.ANOMALY_MASTER_RATIO:
            self.ratio.anomaly_master += stat.value

        elif stat.kind == StatKind.CRIT_RATIO:
            self.flat.crit_ratio += stat.value
        elif stat.kind == StatKind.CRIT_MULTI:
            self.flat.crit_multi += stat.value
        elif stat.kind == StatKind.PEN_RATIO:
            self.flat.pen_ratio += stat.value
        elif stat.kind == StatKind.PEN_FLAT:
            self.flat.pen_flat += stat.value
        elif stat.kind == StatKind.ANOMALY_PROFICIENCY:
            self.flat.anomaly_proficiency += stat.value
        elif stat.kind == StatKind.ACC_RATIO:
            self.flat.acc_ratio += stat.value
        elif stat.kind.startswith(StatKind.DMG_RATIO):
            self.flat.__dict__[stat.kind] += stat.value


@dataclass
class WeaponGrowth:
    atk_rate: float = 0.0
    primary_rate: float = 0.0


@dataclass
class HitContext:
    agent: str = ""  # empty str means that wound apply to all the agents
    tags: set[str] = field(default_factory=set)

    # agent -> moster
    atk_attr: Attribute | None = None
    atk_kind: AttackKind | None = None
    assault: bool | None = None

    # moster
    daze: bool | None = None

    @staticmethod
    def default():
        return HitContext("", set(), None, None, False, False)

    def contains(self, rhs):
        if rhs.agent and self.agent != rhs.agent:
            return False
        if rhs.tags and not self.tags.issuperset(rhs.tags):
            return False
        if rhs.atk_attr and self.atk_attr != rhs.atk_attr:
            return False
        if rhs.atk_kind and self.atk_kind != rhs.atk_kind:
            return False
        if rhs.assault is not None and self.assault != rhs.assault:
            return False
        if rhs.daze is not None and self.daze != rhs.daze:
            return False
        return True


class EnemyModel(BaseModel):
    level: int = 70
    base: int = 60


class AgentBuild(BaseModel):
    agent_name: str = ""
    agent_rep: int = 0
    agent_level: int = 0
    weapon_name: str = ""
    weapon_rep: int = 0
    weapon_level: int = 0
    skills: SkillLevels = SkillLevels()
    discs: DiscGroup = DiscGroup()


class BuffModel(BaseModel):
    idx: int = 0  # 0 for team, 1 for first agent ...
    key: str = ""
    origin_cov: float = 1.0
    cov: float = 1.0
    stat_str: str = ""


class CalcInput(BaseModel):
    agent1: AgentBuild = AgentBuild()
    agent2: AgentBuild = AgentBuild()
    agent3: AgentBuild = AgentBuild()
    enemy: EnemyModel = EnemyModel()
    combo: list[str] = []
    buffs: dict[str, dict] = {}


class ExtraMultiplier:
    @abc.abstractmethod
    def calc(self) -> float:
        pass

    @abc.abstractmethod
    def active(self, anomaly: bool, context: HitContext) -> bool:
        pass

    @abc.abstractmethod
    def show(self) -> str:
        pass
