import math
from functools import reduce

from build import Build, test_build
from model import (
    AgentData,
    ContextData,
    Disc,
    DiscList,
    StatKind,
    StatValue,
    WeaponData,
)


class Number:
    def __init__(self, v=0.0, source=""):
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
        if abs(self.v) > 1.0 or self.v == 0.0:
            return f"{self.v}"
        else:
            return f"{self.v * 100.0:.1f}%"


class LazyAdd:
    def __init__(self, numbers, source=""):
        self.numbers = [Number(n) for n in numbers]
        self.source = source

    def add(self, n):
        self.numbers.append(Number(n))

    def value(self):
        return reduce(lambda x, y: x + y, self.numbers, Number()).value()

    def __str__(self):
        s = "+".join([str(n) for n in self.numbers])
        if len(self.numbers) > 1:
            s = "(" + s + ")"
        return s


# 1.1
class ATK:
    def __init__(self):
        self.agent = Number()
        self.weapon = Number()
        self.static_percent = LazyAdd([1.0])
        self.static_flat = LazyAdd([])
        self.dynamic_percent = LazyAdd([1.0])
        self.dynamic_flat = LazyAdd([])
        pass

    def calc(self):
        return (
            (self.agent + self.weapon) * self.static_percent + self.static_flat
        ) * self.dynamic_percent + self.dynamic_flat

    def __str__(self):
        return f"[ ( {self.agent} + {self.weapon}) * {self.static_percent} + {self.static_flat} ] * {self.dynamic_percent} + {self.dynamic_flat}"


# 1.2
class SkillMultiplier:
    def __init__(self):
        self.value = LazyAdd([1.0])

    def calc(self):
        return self.value

    def __str__(self):
        return f"{self.value}"


# 2
class DMGPercentMultiplier:
    def __init__(self):
        self.item = LazyAdd([1.0])

    def calc(self):
        return self.item

    def __str__(self):
        return f"{self.item}"


# 3
class ResistanceMutiplier:
    def __init__(self):
        self.item = LazyAdd([1.0])

    def calc(self):
        return self.item

    def __str__(self):
        return f"{self.item}"


# 4
class DefenseMultiplier:

    @staticmethod
    def defense_func(level):
        if level > 60:
            level = 60
        return math.floor(0.1551 * level * level + 3.141 * level + 47.2049)

    def __init__(self, **kw):
        self.agent_level = kw.get("agent_level", 50)
        self.enemy_level = kw.get("enemy_level", 70)
        self.enemy_base = kw.get("enemy_base", 50)

        self.agent = Number(self.defense_func(self.agent_level))
        self.enemy = Number(self.defense_func(self.enemy_level) * self.enemy_base / 50)

        self.pen_percent = LazyAdd([])
        self.pen_flat = LazyAdd([0.0])

    def calc(self):
        return self.agent / (
            self.agent + self.enemy * (Number(1.0) - self.pen_percent) - self.pen_flat
        )

    def __str__(self):
        pen = Number(1.0) - self.pen_percent
        return f"( {self.agent} / ({self.agent} + {self.enemy} * {pen} - {self.pen_flat}) )"


# 5
class CriticalMultiplier:

    def __init__(self):
        self.prob = LazyAdd([])
        self.multi = LazyAdd([])

    def calc(self):
        return Number(1.0) + Number(self.prob.value() * self.multi.value())

    def __str__(self):
        return f"(1.0 + {self.prob} * {self.multi})"


# 7
class DazeMultiplier:

    def __init__(self):
        self.multi = LazyAdd([Number(1.0)])

    def calc(self):
        return self.multi

    def __str__(self):
        return f"{self.multi}"


class DMG:
    def __init__(self):
        self.atk = ATK()
        self.skill = SkillMultiplier()
        self.dmg_percent = DMGPercentMultiplier()
        self.resistance = ResistanceMutiplier()
        self.defense = DefenseMultiplier()
        self.critical = CriticalMultiplier()
        self.daze = DazeMultiplier()

    def calc(self, daze=False):
        v = (
            self.atk.calc()
            * self.skill.calc()
            * self.dmg_percent.calc()
            * self.resistance.calc()
            * self.defense.calc()
            * self.critical.calc()
        )
        if daze:
            v *= self.daze.calc()
        return v

    def apply_stat(self, stat: StatValue, source="", dynamic=False):
        number = Number(stat.value, source)
        if stat.kind == StatKind.ATK_PERCENT:
            if dynamic:
                self.atk.dynamic_percent.add(number)
            else:
                self.atk.static_percent.add(number)
        elif stat.kind == StatKind.ATK_FLAT:
            if dynamic:
                self.atk.dynamic_flat.add(number)
            else:
                self.atk.static_flat.add(number)
        elif stat.kind == StatKind.CRIT_PROB:
            self.critical.prob.add(number)
        elif stat.kind == StatKind.CRIT_MULTI:
            self.critical.multi.add(number)
        elif stat.kind == StatKind.PEN_PERCENT:
            self.defense.pen_percent.add(number)
        elif stat.kind == StatKind.PEN_FLAT:
            self.defense.pen_flat.add(number)
        elif stat.kind == StatKind.DMG_PERCENT:
            self.dmg_percent.item.add(number)

    def apply_agent(self, agent: AgentData):
        self.atk.agent = Number(agent.atk, "Agent basic ATK")
        self.defense.agent_level = Number(agent.level)
        self.critical.prob.add(Number(agent.crit_prob, "Agent basic CRIT_PROB"))
        self.critical.multi.add(Number(agent.crit_muilti, "Agent basic CRIT_MULTI"))

    def apply_weapon(self, weapon: WeaponData):
        self.atk.weapon = Number(weapon.atk, "Weapon basic ATK")
        self.apply_stat(weapon.primary, "Weapon primary stat")

    def apply_disc(self, disc: Disc):
        self.apply_stat(disc.primary, f"Disc-{disc.index} {disc.kind} primary")
        for s in disc.secondaries:
            self.apply_stat(s, f"Disc-{disc.index} {disc.kind} secondary")

    def apply_discs(self, discs: DiscList):
        for disc in discs.discs:
            self.apply_disc(disc)

    def apply_build_static(self, b: Build):
        self.apply_agent(b.agent)
        self.apply_weapon(b.weapon)
        self.apply_discs(b.discs)

    def apply_build_dynamic(self, b: Build, context: ContextData):
        for buff in b.buffs:
            stat = buff.produce(context)
            if stat:
                self.apply_stat(stat, source=buff.source, dynamic=True)

    def apply_build_all(self, b: Build, context: ContextData):
        self.apply_build_static(b)
        self.apply_build_dynamic(b, context)
        if context.daze:
            self.daze.multi.add(Number(context.daze, "Basic daze ratio"))

    def __str__(self):
        return (
            f"{self.atk}             \t# base\n"
            + f"* {self.skill}       \t# skill\n"
            + f"* {self.dmg_percent} \t# dmg_percent\n"
            + f"* {self.resistance}  \t# resistance\n"
            + f"* {self.defense}     \t# defense\n"
            + f"* {self.critical}    \t# critical\n"
            + f"* {self.daze}        \t# daze\n"
            + f"= {self.calc()}"
        )


def test_dmg():
    dmg = DMG()
    build = test_build()
    context = ContextData()
    dmg.apply_build_all(build, context)
    print(build)
    print(dmg)


if __name__ == "__main__":
    test_dmg()
