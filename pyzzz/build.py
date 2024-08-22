from pyzzz.model import *


@dataclass
class SummaryBuild:
    agent_name: str = ""
    agent_level: int = 60
    agent_asc: bool = False
    agent_rep: int = 0
    skill_levels: SkillLevels = field(default_factory=SkillLevels)

    weapon_name: str = ""
    weapon_level: int = 60
    weapon_rep: int = 1

    crit_ratio: float = 0.05
    crit_multi: float = 0.50
    green_atk: float = 0

    suit2: list[DiscKind] = field(default_factory=list)
    suit4: DiscKind | None = None
    disc4: StatKind = StatKind.CRIT_RATIO
    disc5: StatKind = StatKind.DMG_RATIO
    disc6: StatKind = StatKind.ATK_RATIO

    enemy_level: int = 60
    enemy_base: int = 60
    team: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class FullBuild:
    agent_name: str = ""
    agent_level: int = 60
    agent_asc: bool = False
    agent_rep: int = 0
    skill_levels: SkillLevels = field(default_factory=SkillLevels)

    weapon_name: str = ""
    weapon_level: int = 60
    weapon_rep: int = 1

    discs: DiscGroup = field(default_factory=DiscGroup)

    enemy_level: int = 60
    enemy_base: int = 60
    team: dict[str, dict[str, str]] = field(default_factory=dict)
