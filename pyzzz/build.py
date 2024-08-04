from pyzzz.agents import Agent
from pyzzz.buff import Buff
from pyzzz.discs import get_suit2_stat, get_suit4_buff
from pyzzz.model import *
from pyzzz.weapons import Weapon, get_weapon


class Build:

    def __init__(self):
        self.summary = False
        self.agent = Agent()
        self.weapon = Weapon()
        self.discs = DiscGroup()
        self.teams: list[Agent] = []
        self.buffs: dict[str, Buff] = {}
        self.extra: list[StatValue] = []

    def build_teams(self, teams: list[Agent]):
        self.teams = teams

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

        for b in self.weapon.buffs:
            self.add_buff(b)

        for agent in self.teams:
            for b in agent.buffs():
                self.add_buff(b)

    def replace_extra(self, extra):
        self.extra = extra
        return self

    def replace_weapon(self, weapon: Weapon):
        if not self.summary:
            self.weapon = weapon
            return

        # need calc delta
        atk_delta = weapon.origin_data.atk - self.weapon.origin_data.atk
        self.agent.data.atk += atk_delta

        self.discs.summary.secondaries.append(
            self.weapon.origin_data.primary.negative()
        )
        self.discs.summary.secondaries.append(weapon.origin_data.primary)

    def replace_disc(self, disc: Disc):
        if not self.summary:
            self.discs.set(disc.index, disc)
            self.collect_buffs()
            return

        raise Exception("cannot replace disc under summary mode")

    def __str__(self):
        s = (
            f"Build:\n"
            + f"{self.agent.data}\n"
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


def test_build_summary():
    from pyzzz import agents

    b = Build()
    b.summary = True

    b.agent = agents.Ellen(60, skill_levels=SkillLevels(4, 9, 9, 9, 9, 9))
    b.agent.data.level = 50
    b.agent.data.atk = 1278
    b.agent.data.crit_ratio = 88.2 / 100
    b.agent.data.crit_multi = 78.8 / 100

    b.weapon = get_weapon("CannonRotor", cov=1.0)
    b.weapon.data = WeaponData(0, 0, StatValue.empty())

    disc = Disc(0, DiscKind.Summary, StatValue.empty())
    disc.secondaries.append(StatValue(sum([1330]), StatKind.ATK_FLAT))
    b.discs.make_summary(
        disc, [DiscKind.Polar_Metal, DiscKind.Woodpecker_Electro], DiscKind.Polar_Metal
    )
    b.discs.at(5).primary.kind = StatKind.ATK_RATIO

    b.build_teams([b.agent, agents.Soukaku(core_skill_atk=900), agents.Lycaon()])

    b.collect_buffs()

    return b


if __name__ == "__main__":
    print(test_build_summary())
