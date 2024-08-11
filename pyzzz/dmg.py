import copy
import math
from dataclasses import replace
from functools import reduce
from typing import Optional, Union

from pyzzz import build, weapons
from pyzzz.build import Build
from pyzzz.model import *


class Number:
    def __init__(self, v, source=""):
        if isinstance(v, Number):
            self.v = v.value()
            self.source = v.source
        else:
            self.v = v
            self.source = ""
        if source:
            self.source = source

    def __add__(self, rhs):
        return Number(self.v + rhs.value())

    def __mul__(self, rhs):
        return Number(self.v * rhs.value())

    def __sub__(self, rhs):
        return Number(self.v - rhs.value())

    def __truediv__(self, rhs):
        return Number(self.v / rhs.value())

    def __neg__(self):
        return Number(-self.v)

    def value(self):
        return self.v

    def __str__(self):
        # return f"{self.v:.3f}".rstrip("0").rstrip(".")
        if abs(self.v) > 1.0 or self.v == 0.0:
            return f"{self.v:.3f}".rstrip("0").rstrip(".")
        else:
            return f"{self.v * 100.0:.1f}%"


class LazyAdd:
    def __init__(self, numbers, source=""):
        self.numbers = [Number(n) for n in numbers]
        self.source = source

    def add(self, n: Union[float, Number]):
        self.numbers.append(Number(n))

    def set(self, n: Union[float, Number]):
        self.numbers = [Number(n)]

    def value(self):
        return reduce(lambda x, y: x + y, self.numbers, Number(0.0)).value()

    def __str__(self):
        if not self.numbers:
            return "0"
        s = "+".join([str(n) for n in self.numbers])
        if len(self.numbers) > 1:
            s = "(" + s + ")"
        return s


class ListMultiplier(LazyAdd):
    def __init__(self, numbers=None):
        if not numbers:
            numbers = [1.0]
        LazyAdd.__init__(self, numbers)

    def calc(self):
        return self


# 1.1
class ATK:
    def __init__(self):
        self.agent = Number(0.0)
        self.weapon = Number(0.0)
        self.static_ratio = LazyAdd([1.0])
        self.static_flat = LazyAdd([])
        self.dynamic_ratio = LazyAdd([1.0])
        self.dynamic_flat = LazyAdd([])

    def calc(self):
        return (
            (self.agent + self.weapon) * self.static_ratio + self.static_flat
        ) * self.dynamic_ratio + self.dynamic_flat

    def __str__(self):
        return f"( ( ({self.agent} + {self.weapon}) * {self.static_ratio} + {self.static_flat} ) * {self.dynamic_ratio} + {self.dynamic_flat} )"


# 1.2
SkillMultiplier = ListMultiplier

# 2
DMGMultiplier = ListMultiplier

# 3
ResistanceMutiplier = ListMultiplier


# 4
class DefenseMultiplier:

    @staticmethod
    def defense_func(level):
        if level > 60:
            level = 60
        return math.floor(0.1551 * level * level + 3.141 * level + 47.2049)

    def __init__(self, **kw):
        self._agent_level = kw.get("agent_level", 60)
        self._enemy_level = kw.get("enemy_level", 70)
        self._enemy_base = kw.get("enemy_base", 50)

        self.agent = Number(self.defense_func(self._agent_level))
        self.enemy = Number(
            self.defense_func(self._enemy_level) * self._enemy_base / 50
        )

        self.pen_ratio = LazyAdd([])
        self.pen_flat = LazyAdd([0.0])

    def set_agent_level(self, level):
        self._agent_level = level
        self.agent = Number(self.defense_func(self._agent_level))

    def set_enemy_level(self, level):
        self._enemy_level = level
        self.enemy = Number(self.defense_func(self._enemy_level))

    def calc(self):
        return self.agent / (
            self.agent + self.enemy * (Number(1.0) - self.pen_ratio) - self.pen_flat
        )

    def __str__(self):
        pen = Number(1.0) - self.pen_ratio
        return f"( {self.agent} / ({self.agent} + {self.enemy} * {pen} - {self.pen_flat}) )"


# 5
class CriticalMultiplier:

    def __init__(self):
        self.ratio = LazyAdd([])
        self.multi = LazyAdd([])

    def calc(self):
        ratio = self.ratio.value()
        if ratio > 1.0:
            ratio = 1.0
        return Number(1.0) + Number(ratio * self.multi.value())

    def __str__(self):
        ratio = self.ratio.value()
        if ratio > 1.0:
            return f"(1.0 + 1.0 * {self.multi})"
        else:
            return f"(1.0 + {self.ratio} * {self.multi})"


# 7
DazeMultiplier = ListMultiplier


class DMG:
    def __init__(self):
        self.atk = ATK()
        self.skill = SkillMultiplier()
        self.dmg_ratio = DMGMultiplier()
        self.resistance = ResistanceMutiplier()
        self.defense = DefenseMultiplier()
        self.critical = CriticalMultiplier()
        self.daze = DazeMultiplier()

    def calc(self):
        v = (
            self.atk.calc()
            * self.skill.calc()
            * self.dmg_ratio.calc()
            * self.resistance.calc()
            * self.defense.calc()
            * self.critical.calc()
            * self.daze.calc()
        )
        return v

    def apply_stat(self, stat: StatValue, source="", dynamic=False):
        number = Number(stat.value, source)
        if stat.kind == StatKind.ATK_RATIO:
            if dynamic:
                self.atk.dynamic_ratio.add(number)
            else:
                self.atk.static_ratio.add(number)
        elif stat.kind == StatKind.ATK_FLAT:
            if dynamic:
                self.atk.dynamic_flat.add(number)
            else:
                self.atk.static_flat.add(number)
        elif stat.kind == StatKind.CRIT_RATIO:
            self.critical.ratio.add(number)
        elif stat.kind == StatKind.CRIT_MULTI:
            self.critical.multi.add(number)
        elif stat.kind == StatKind.PEN_RATIO:
            self.defense.pen_ratio.add(number)
        elif stat.kind == StatKind.PEN_FLAT:
            self.defense.pen_flat.add(number)
        elif stat.kind == StatKind.DMG_RATIO:
            self.dmg_ratio.add(number)
        elif stat.kind == StatKind.RES_RATIO:
            self.resistance.add(number)
        elif stat.kind == StatKind.STUN_DMG_RATIO:
            self.daze.add(number)

    def apply_agent_data(self, agent: AgentData):
        self.atk.agent = Number(agent.atk_base, "Agent basic ATK")
        self.defense.set_agent_level(agent.level)
        self.critical.ratio.add(Number(agent.crit_ratio, "Agent basic CRIT_RATIO"))
        self.critical.multi.add(Number(agent.crit_multi, "Agent basic CRIT_MULTI"))

    def apply_weapon_data(self, weapon: WeaponData):
        self.atk.weapon = Number(weapon.atk, "Weapon basic ATK")
        self.apply_stat(weapon.primary, "Weapon primary stat")

    def apply_disc(self, disc: Disc):
        self.apply_stat(disc.primary, f"Disc-{disc.index} {disc.kind} primary")
        for s in disc.secondaries:
            self.apply_stat(s, f"Disc-{disc.index} {disc.kind} secondary")

    def apply_discs(self, discs: DiscGroup):
        for s in discs.suit2_stats:
            self.apply_stat(s)

        if discs.summary:
            self.apply_disc(discs.summary)
            return

        for disc in discs.discs:
            if not disc.empty():
                self.apply_disc(disc)

    def apply_build_static(self, b: Build):
        self.apply_agent_data(b.agent.base)
        self.apply_weapon_data(b.weapon.data)
        self.apply_discs(b.discs)
        for stat in b.extra:
            self.apply_stat(stat)

    def apply_build_dynamic(self, b: Build, context: ContextData):
        if context.daze:
            self.daze.add(Number(0.5, "Basic daze ratio"))
        for buff in b.buffs.values():
            stat = buff.produce(context)
            if stat:
                self.apply_stat(stat, source=buff.source, dynamic=True)

    def apply_build_all(self, b: Build, context: ContextData):
        self.apply_build_static(b)
        self.apply_build_dynamic(b, context)

    def one_line(self):
        return f"{self.atk} * {self.skill} * {self.dmg_ratio} * {self.resistance} * {self.defense} * {self.critical} * {self.daze} = {self.calc()}"

    def __str__(self):
        return (
            f"{self.atk}             \t# base\n"
            + f"* {self.skill}       \t# skill\n"
            + f"* {self.dmg_ratio} \t# dmg_ratio\n"
            + f"* {self.resistance}  \t# resistance\n"
            + f"* {self.defense}     \t# defense\n"
            + f"* {self.critical}    \t# critical\n"
            + f"* {self.daze}        \t# daze\n"
            + f"= {self.calc()}"
        )


class Combo:
    def __init__(
        self,
        attacks: AttackList,
        build: Build,
        context: Optional[ContextData] = None,
    ):
        if not context:
            context = ContextData()

        self.attacks = attacks
        self.build = build
        self.context = context
        self.dmgs = []

    def calc(self, build=None, context=None):
        if not build:
            build = self.build
        if not context:
            context = self.context

        base_dmg = DMG()
        base_dmg.apply_build_static(build)

        self.dmgs = []
        for attack_cb in self.attacks.attacks:
            attack = attack_cb(build.agent)

            c = copy.deepcopy(context)
            c.atk_kind = attack.kind
            c.atk_attr = attack.attribute

            dmg = copy.deepcopy(base_dmg)
            dmg.apply_build_dynamic(build, c)
            dmg.skill.set(attack.multi)
            self.dmgs.append(dmg)

        value = 0.0
        for dmg in self.dmgs:
            value += dmg.calc().value()
        return value

    def delta(self):
        print(self.build)

        base = self.calc()
        print(self)
        print(f"base line {self.attacks} : {base}")

        def impl(extra):
            build = copy.copy(self.build).replace_extra(extra)
            build.calc_static_agent()
            build.collect_buffs()
            new = self.calc(build, self.context)
            print(self)
            print(f"delta ratio : {(new / base - 1) * 100.0 :.3f}% , by {extra}\n")

        impl([StatValue(9, StatKind.PEN_FLAT)])
        impl([StatValue(19, StatKind.ATK_FLAT)])
        impl([StatValue(0.03, StatKind.ATK_RATIO)])
        impl([StatValue(0.03, StatKind.DMG_RATIO)])
        impl([StatValue(0.024, StatKind.CRIT_RATIO)])
        impl([StatValue(-0.024, StatKind.CRIT_RATIO)])
        impl([StatValue(0.048, StatKind.CRIT_MULTI)])
        impl([StatValue(0.024, StatKind.PEN_RATIO)])

        disc4 = self.build.discs.at(4).primary
        if disc4.kind == StatKind.CRIT_RATIO:
            impl(
                [
                    StatValue(-0.24, StatKind.CRIT_RATIO),
                    StatValue(+0.48, StatKind.CRIT_MULTI),
                ]
            )
        elif disc4.kind == StatKind.CRIT_MULTI:
            impl(
                [
                    StatValue(+0.24, StatKind.CRIT_RATIO),
                    StatValue(-0.48, StatKind.CRIT_MULTI),
                ]
            )

        disc5 = self.build.discs.at(5).primary
        if disc5.kind == StatKind.ATK_RATIO:
            impl(
                [
                    StatValue(-0.3, StatKind.ATK_RATIO),
                    StatValue(0.3, StatKind.DMG_RATIO),
                ]
            )
            impl(
                [
                    # self.build.discs.suit2_stats[0].negative(),
                    StatValue(-0.3, StatKind.ATK_RATIO),
                    StatValue(0.24, StatKind.PEN_RATIO),
                ]
            )
        elif disc5.kind == StatKind.DMG_RATIO:
            impl(
                [
                    StatValue(-0.3, StatKind.DMG_RATIO),
                    StatValue(0.3, StatKind.ATK_RATIO),
                ]
            )
            impl(
                [
                    # self.build.discs.suit2_stats[0].negative(),
                    StatValue(-0.3, StatKind.DMG_RATIO),
                    StatValue(0.24, StatKind.PEN_RATIO),
                ]
            )
        elif disc5.kind == StatKind.PEN_RATIO:
            impl(
                [
                    StatValue(+0.3, StatKind.DMG_RATIO),
                    StatValue(-0.24, StatKind.PEN_RATIO),
                ]
            )
            impl(
                [
                    StatValue(+0.3, StatKind.ATK_RATIO),
                    StatValue(-0.24, StatKind.PEN_RATIO),
                ]
            )


        def level_up(level=60):
            build = copy.deepcopy(self.build)
            agent_new = copy.deepcopy(build.agent).set_stats(level)
            agent_old = copy.deepcopy(build.agent).set_stats(build.agent.level)
            build.agent.base.level = level
            build.agent.base = build.agent.base + (agent_new.base - agent_old.base)
            build.calc_static_agent()

            new = self.calc(build, self.context)
            print(self)
            print(
                f"delta ratio : {(new / base - 1) * 100.0 :.3f}% , by agent level {build.agent.level}->{level}\n"
            )

        if self.build.agent.static.level < 60:
            level_up(60)

        def weapon60():
            build = copy.deepcopy(self.build)
            weapon_new = copy.deepcopy(build.weapon)
            weapon_new.set_stats(60)
            weapon_old = copy.deepcopy(build.weapon)
            weapon_old.set_stats(build.weapon._level)

            build.weapon.data.level = 60
            build.weapon.data = build.weapon.data + (weapon_new.data - weapon_old.data)
            build.calc_static_agent()

            new = self.calc(build, self.context)
            print(self)
            print(
                f"delta ratio : {(new / base - 1) * 100.0 :.3f}% , by weapon L50->L60\n"
            )

        if self.build.weapon.data.level < 60:
            weapon60()

        def core():
            skills = self.build.agent.skill_levels
            build = copy.deepcopy(self.build)
            build.agent.set_stats(skill_levels=replace(skills, core=skills.core + 1))
            build.calc_static_agent()
            build.collect_buffs()

            new = self.calc(build, self.context)
            print(self)
            print(
                f"delta ratio : {(new / base - 1) * 100.0 :.3f}% , by core {skills.core}->{skills.core+1}\n"
            )

        core()

        def basic():
            skills = self.build.agent.skill_levels
            build = copy.deepcopy(self.build)
            build.agent.set_stats(skill_levels=replace(skills, basic=skills.basic + 1))
            new = self.calc(build, self.context)
            print(self)
            print(
                f"delta ratio : {(new / base - 1) * 100.0 :.3f}% , by basic {skills.basic}->{skills.basic+1}\n"
            )

        basic()

        # def deep_sea():
        #     build = copy.deepcopy(self.build).replace_weapon(
        #         weapons.create_weapon("DeepSeaVisitor")
        #     )
        #     build.replace_extra([
        #             StatValue(-0.24, StatKind.CRIT_RATIO),
        #             StatValue(+0.48, StatKind.CRIT_MULTI),
        #             self.build.discs.suit2_stats[0].negative(),
        #             StatValue(-0.3, StatKind.ATK_RATIO),
        #             StatValue(0.32, StatKind.PEN_RATIO),
        #         ])
        #     print(build)
        #     new = self.calc(build, self.context)
        #     print(self)
        #     print(
        #         f"delta ratio : {(new / base - 1) * 100.0 :.3f}% , by weapon deep sea\n"
        #     )
        # deep_sea()

    def __str__(self):
        v = 0.0
        s = ""
        for dmg in self.dmgs:
            v += dmg.calc().value()
            s += str(dmg.one_line())
            s += "\n"
        s += f"In total = {v}"
        return s


def test_combo():
    from pyzzz.agents.ellen import Ellen

    # attacks = AttackList([Ellen.Final])
    # b = build.test_build_full()
    # b.collect_buffs()
    # combo = Combo(attacks, b)
    # combo.delta()

    # attacks = AttackList([Ellen.EX1, Ellen.A3])
    # b = build.test_build_full()
    # b.collect_buffs()
    # combo = Combo(attacks, b)
    # combo.delta()

    attacks = AttackList([Ellen.A1, Ellen.A2, Ellen.A3])
    b = build.test_build_full()
    b.collect_buffs()
    combo = Combo(attacks, b)
    combo.delta()

    # attacks = AttackList([Ellen.Chain])
    # b = build.test_build_full()
    # b.collect_buffs()
    # combo = Combo(attacks, b)
    # combo.delta()


def test_combo2():
    from pyzzz.agents.soukaku import Soukaku

    # attacks = AttackList([Soukaku.A1, Soukaku.A2, Soukaku.A3])
    attacks = AttackList([Soukaku.Dodge, Soukaku.A3])
    # attacks = AttackList([Soukaku.Chain])
    b = build.test_build_full2()
    b.collect_buffs()
    combo = Combo(attacks, b)
    combo.delta()


def test_combo3():
    from pyzzz.agents.lycaon import Lycaon

    attacks = AttackList([Lycaon.Chain])
    b = build.test_build_full3()
    b.collect_buffs()
    combo = Combo(attacks, b)
    combo.delta()


if __name__ == "__main__":
    test_combo2()
