from pyzzz import agents, weapons
from pyzzz.agents.agent import Agent
from pyzzz.buff import Buff
from pyzzz.discs import get_suit2_stat, get_suit4_buff
from pyzzz.model import *
from pyzzz.weapons import Weapon


@dataclass
class SummaryData:
    agent_name: str = ""
    agent_level: int = 60
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

    team: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class FullData:
    agent_name: str = ""
    agent_level: int = 60
    agent_rep: int = 0
    skill_levels: SkillLevels = field(default_factory=SkillLevels)

    weapon_name: str = ""
    weapon_level: int = 60
    weapon_rep: int = 1

    discs: DiscGroup = field(default_factory=DiscGroup)
    team: dict[str, dict[str, str]] = field(default_factory=dict)


class Build:

    def __init__(self):
        self.summary = False
        self.agent = Agent()
        self.weapon = Weapon()
        self.discs = DiscGroup()
        self.team: list[Agent] = []
        self.buffs: dict[str, Buff] = {}
        self.extra: list[StatValue] = []

    def build_team(self, team: list[Agent]):
        self.team = team

    def calc_static_agent(self):
        self.agent.set_weapon(self.weapon.data)
        self.agent.calc_static(self.discs, self.extra)
        return self

    def add_buff(self, b):
        self.buffs[b.source] = b

    def collect_buffs(self):
        self.buffs = {}
        self.discs.suit2_stats = []

        for k in self.discs.suit2:
            stat = get_suit2_stat(k)
            if stat:
                self.discs.suit2_stats.append(stat)

        buf = get_suit4_buff(self.discs.suit4)
        if buf:
            self.add_buff(buf)

        for b in self.weapon.buffs():
            self.add_buff(b)

        for agent in self.team:
            for b in agent.buffs():
                self.add_buff(b)

    @staticmethod
    def from_summary(summary: SummaryData):
        b = Build()
        b.summary = True
        b.agent = agents.create_agent(
            summary.agent_name,
            level=summary.agent_level,
            skill_levels=summary.skill_levels,
            repetition=summary.agent_rep,
        )
        b.weapon = weapons.create_weapon(
            summary.weapon_name,
            level=summary.weapon_level,
            repetition=summary.weapon_rep,
        )
        disc = Disc(0, DiscKind.Summary, StatValue.create_empty())
        disc.secondaries.append(StatValue(summary.green_atk, StatKind.ATK_FLAT))
        b.discs.at(4).primary.kind = summary.disc4
        b.discs.at(5).primary.kind = summary.disc5
        b.discs.at(6).primary.kind = summary.disc6
        b.discs.make_summary(disc, summary.suit2, summary.suit4)

        b.agent.base.crit_ratio = summary.crit_ratio  # set fixed value
        b.agent.base.crit_multi = summary.crit_multi  # set fixed value
        b.weapon.data.primary.value = 0.0  # clear weapon primary

        b.agent.set_weapon(b.weapon.data)
        b.agent.calc_static(b.discs)

        team = [b.agent]
        for name, extra in summary.team.items():
            agent = agents.create_agent(name, **extra)
            team.append(agent)
        b.build_team(team)

        b.collect_buffs()

        return b

    @staticmethod
    def from_full(full: FullData):
        b = Build()
        b.agent = agents.create_agent(
            full.agent_name,
            level=full.agent_level,
            skill_levels=full.skill_levels,
            repetition=full.agent_rep,
        )
        b.weapon = weapons.create_weapon(
            full.weapon_name, level=full.weapon_level, repetition=full.weapon_rep
        )

        b.discs = full.discs
        b.discs.generate_suits()
        b.agent.set_weapon(b.weapon.data)
        b.agent.calc_static(b.discs)

        team = [b.agent]
        for name, extra in full.team.items():
            agent = agents.create_agent(name, **extra)
            team.append(agent)
        b.build_team(team)

        b.collect_buffs()
        return b

    def replace_extra(self, extra):
        self.extra = extra
        return self

    def replace_weapon(self, weapon):
        if self.summary:
            raise Exception("cannot replace weapon under summary mode")
        self.weapon = weapon
        self.collect_buffs()
        return self

    def replace_disc(self, disc: Disc):
        if self.summary:
            raise Exception("cannot replace disc under summary mode")
        self.discs.set(disc)
        self.collect_buffs()
        return self

    def __str__(self):
        s = (
            f"Build:\n"
            + f"{self.agent.static}\n"
            + f"{self.agent.skill_levels}\n"
            + f"{self.weapon.data}\n"
            + f"{self.discs}\n"
        )
        if self.buffs:
            s += "Buffs:\n"
            for buff in self.buffs.values():
                s += f"\t{buff}\n"
        if self.extra:
            s += "Extra:\n"
            for extra in self.extra:
                s += f"\t{extra}\n"
        return s


def test_build_summary2():
    s = SummaryData()
    s.agent_name = "Ellen"
    s.agent_level = 50
    s.skill_levels = SkillLevels(4, 9, 9, 9, 9, 9)
    s.weapon_name = "CannonRotor"
    s.weapon_level = 50
    s.crit_ratio = 88.2 / 100
    s.crit_multi = 78.8 / 100
    s.green_atk = 1330
    s.suit2 = [DiscKind.Polar_Metal, DiscKind.Woodpecker_Electro]
    s.suit4 = DiscKind.Polar_Metal
    s.disc4 = StatKind.CRIT_RATIO
    s.disc5 = StatKind.ATK_RATIO
    s.team = {"Soukaku": dict(core_skill_atk="1000"), "Lycaon": {}}

    import json
    from dataclasses import asdict

    print(json.dumps(asdict(s), indent=2))

    return Build.from_summary(s)


def test_build_full():
    f = FullData()
    f.agent_name = "Ellen"
    f.agent_level = 60
    f.skill_levels = SkillLevels(5, 10, 10, 10, 10, 10)
    f.weapon_name = "CannonRotor"
    f.weapon_level = 60
    f.discs.set(
        Disc(
            1,
            DiscKind.Woodpecker_Electro,
            StatValue.create_empty(),
            [
                StatValue(0.144, StatKind.CRIT_MULTI),
                StatValue(0.072, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            2,
            DiscKind.Woodpecker_Electro,
            StatValue(316, StatKind.ATK_FLAT),
            [
                StatValue(0.072, StatKind.CRIT_RATIO),
                StatValue(0.06, StatKind.ATK_RATIO),
                StatValue(0.048, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            3,
            DiscKind.Polar_Metal,
            StatValue.create_empty(),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            4,
            DiscKind.Polar_Metal,
            StatValue(0.48, StatKind.CRIT_MULTI),
            # [
            #     StatValue(0.03, StatKind.ATK_RATIO),
            #     StatValue(18, StatKind.PEN_FLAT),
            #     StatValue(0.048, StatKind.CRIT_RATIO),
            #     StatValue(57, StatKind.ATK_FLAT),
            # ],
            [
                StatValue(0.12, StatKind.ATK_RATIO),
                StatValue(19, StatKind.PEN_FLAT),
                StatValue(0.024, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            5,
            DiscKind.Polar_Metal,
            StatValue(0.30, StatKind.ATK_RATIO),
            [
                StatValue(19, StatKind.ATK_FLAT),
                StatValue(0.048, StatKind.CRIT_RATIO),
                StatValue(18, StatKind.PEN_FLAT),
                StatValue(0.144, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            6,
            DiscKind.Polar_Metal,
            StatValue(0.30, StatKind.ATK_RATIO),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
            ],
        )
    )
    # f.team = {"Soukaku": dict(core_skill_atk="1000"), "Lycaon": {}}
    return Build.from_full(f)


def test_build_full2():
    f = FullData()
    f.agent_name = "Soukaku"
    f.agent_level = 60
    f.agent_rep = 6
    f.skill_levels = SkillLevels(4, 10, 10, 10, 10, 10)
    f.weapon_name = "BashfulDemon"
    f.weapon_level = 60
    f.discs.set(
        Disc(
            1,
            DiscKind.Woodpecker_Electro,
            StatValue.create_empty(),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            2,
            DiscKind.Woodpecker_Electro,
            StatValue(316, StatKind.ATK_FLAT),
            [
                StatValue(0.048, StatKind.CRIT_MULTI),
                StatValue(0.09, StatKind.ATK_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            3,
            DiscKind.Polar_Metal,
            StatValue.create_empty(),
            [
                StatValue(0.048, StatKind.CRIT_MULTI),
                StatValue(0.09, StatKind.ATK_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            4,
            DiscKind.Polar_Metal,
            StatValue(0.24, StatKind.CRIT_RATIO),
            [
                StatValue(38, StatKind.ATK_FLAT),
            ],
        )
    )
    f.discs.set(
        Disc(
            5,
            DiscKind.Polar_Metal,
            StatValue(0.24, StatKind.PEN_RATIO),
            [
                StatValue(0.06, StatKind.ATK_RATIO),
                StatValue(0.144, StatKind.CRIT_MULTI),
            ],
            # StatValue(0.30, StatKind.DMG_RATIO),
            # [
            #     StatValue(27, StatKind.PEN_FLAT),
            #     StatValue(0.024, StatKind.CRIT_RATIO),
            # ],
        )
    )
    f.discs.set(
        Disc(
            6,
            DiscKind.Polar_Metal,
            StatValue(0.30, StatKind.ATK_RATIO),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.024, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.team = {"Lycaon": {}}
    return Build.from_full(f)


def test_build_full3():
    f = FullData()
    f.agent_name = "Lycaon"
    f.agent_level = 60
    f.agent_rep = 6
    f.skill_levels = SkillLevels(4, 10, 10, 10, 10, 10)
    f.weapon_name = "PreciousFossilizedCore"
    f.weapon_level = 60
    f.discs.set(
        Disc(
            1,
            DiscKind.Woodpecker_Electro,
            StatValue.create_empty(),
            [
                StatValue(0.144, StatKind.CRIT_MULTI),
                StatValue(0.072, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            2,
            DiscKind.Woodpecker_Electro,
            StatValue(316, StatKind.ATK_FLAT),
            [
                StatValue(0.072, StatKind.CRIT_RATIO),
                StatValue(0.06, StatKind.ATK_RATIO),
                StatValue(0.048, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            3,
            DiscKind.Polar_Metal,
            StatValue.create_empty(),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            4,
            DiscKind.Polar_Metal,
            StatValue(0.24, StatKind.CRIT_RATIO),
            # [
            #     StatValue(0.03, StatKind.ATK_RATIO),
            #     StatValue(18, StatKind.PEN_FLAT),
            #     StatValue(0.048, StatKind.CRIT_RATIO),
            #     StatValue(57, StatKind.ATK_FLAT),
            # ],
            # [
            #     StatValue(0.12, StatKind.ATK_RATIO),
            #     StatValue(19, StatKind.PEN_FLAT),
            #     StatValue(0.024, StatKind.CRIT_RATIO),
            # ],
        )
    )
    f.discs.set(
        Disc(
            5,
            DiscKind.Polar_Metal,
            StatValue(0.30, StatKind.DMG_RATIO),
            [
                StatValue(19, StatKind.ATK_FLAT),
                StatValue(0.048, StatKind.CRIT_RATIO),
                StatValue(18, StatKind.PEN_FLAT),
                StatValue(0.144, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            6,
            DiscKind.Polar_Metal,
            StatValue(0.30, StatKind.IMPACT),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.team = {}
    return Build.from_full(f)


if __name__ == "__main__":
    print(test_build_full2())
