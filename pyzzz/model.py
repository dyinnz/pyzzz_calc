from dataclasses import asdict, dataclass, field
from enum import StrEnum, auto


class StatKind(StrEnum):
    STAT_EMPTY = auto()

    ATK_PERCENT = auto()
    ATK_FLAT = auto()
    CRIT_PROB = auto()
    CRIT_MULTI = auto()
    HP_PERCENT = auto()
    HP_FLAT = auto()
    DEF_PERCENT = auto()
    DEF_FLAT = auto()
    PEN_PERCENT = auto()
    PEN_FLAT = auto()
    ANOMALY = auto()

    DMG_PERCENT = auto()  # TODO: support different DMG


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
            return f"{self.kind}:{self.value}"
        else:
            return f"{self.kind}:{self.value * 100.0:.1f}%"


class Attribute(StrEnum):
    Physical = auto()
    Fire = auto()
    Ice = auto()
    Electric = auto()
    Ether = auto()


class AttackKind(StrEnum):
    Basic = auto()
    Dodge = auto()  # 闪避反击
    Assit = auto()  # 支援攻击
    Special = auto()
    SpecialEx = auto()
    Chain = auto()
    Final = auto()


class DiscKind(StrEnum):
    Empty = auto()

    # see https://zzz.hakush.in/equipment
    FangedMetal = auto()
    PolarMetal = auto()
    ThunderMetal = auto()
    ChaoticMetal = auto()
    InfernoMetal = auto()
    SwingJazz = auto()
    SoulRock = auto()
    HormonePunk = auto()
    FreedomBlues = auto()
    ShockstarDisco = auto()
    PufferElectro = auto()
    WoodpeckerElectro = auto()

    def __repr__(self):
        return f"Disk.{self.name}"


@dataclass
class Disc:
    index: int
    kind: DiscKind
    primary: StatValue
    secondaries: list[StatValue] = field(default_factory=list)


@dataclass
class DiscList:
    discs: list[Disc]

    suit2: list[DiscKind] = field(default_factory=list)
    suit4: DiscKind = DiscKind.Empty

    def append(self, d: Disc):
        self.discs.append(d)

    def __repr__(self):
        s = "Discs:\n"
        for disc in self.discs:
            s += f"\t{disc}\n"
        s += "\tSuit2: <"
        s += ", ".join([str(k) for k in self.suit2])
        s += f">\tSuit4: {self.suit4}"
        return s


@dataclass
class SkillData:
    core: int = 0
    basic: int = 0
    dodge: int = 0
    special: int = 0
    chain: int = 0
    assit: int = 0


@dataclass
class AgentData:
    level: int
    atk: float
    crit_prob: float = 0.05
    crit_muilti: float = 0.50
    skill: SkillData = field(default_factory=SkillData)


@dataclass
class WeaponData:
    level: int
    atk: float
    primary: StatValue


@dataclass
class ContextData:
    # agent -> moster
    atk_attr: Attribute = Attribute.Physical
    atk_kind: AttackKind = AttackKind.Basic
    assault: bool = False

    # moster
    daze: float = 0.0


if __name__ == "__main__":
    stat = StatValue(1.0, StatKind.STAT_EMPTY)
    dt = asdict(stat)
    import json

    print(stat, json.dumps(asdict(stat)))
