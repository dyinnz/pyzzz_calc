import abc
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
        self._enemy_base = kw.get("enemy_base", 54)

        self.agent = Number(self.defense_func(self._agent_level))
        self.enemy = Number(
            self.defense_func(self._enemy_level) * self._enemy_base / 50
        )

        self.pen_ratio = LazyAdd([])
        self.pen_flat = LazyAdd([0.0])

    def set_agent(self, level):
        self._agent_level = level
        self.agent = Number(self.defense_func(self._agent_level))

    def set_enemy(self, level, base):
        self._enemy_level = level
        self._enemy_base = base
        self.enemy = Number(
            self.defense_func(self._enemy_level) * self._enemy_base / 50
        )

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


# ap
class AnomalyProficiencyMultiplier(LazyAdd):
    def __init__(self):
        LazyAdd.__init__(self, [0.0])

    def calc(self):
        return Number(self.value() / 100.0)

    def __str__(self):
        return f"({super().__str__()} / 100.0)"


class AnomalyAttributeMultiplier:
    def __init__(self):
        self.attribute = Attribute.All
        pass

    def calc(self):
        v = 0.0
        if self.attribute == Attribute.Fire:
            v = 0.5 * 20
        elif self.attribute == Attribute.Electric:
            v = 1.25 * 10
        elif self.attribute == Attribute.Ether:
            v = 0.625 * 20
        elif self.attribute == Attribute.Ice:
            v = 5
        elif self.attribute == Attribute.Physical:
            v = 7.13
        return Number(v)

    def __str__(self):
        return f"{self.calc()}"


class AnomalyLevelMultiplier:
    def __init__(self):
        self.level = 60
        pass

    def calc(self):
        return Number(round(1 + 1 / 59 * (self.level - 1), 4))

    def __str__(self):
        return f"{self.calc()}"


class DMG:
    def __init__(self):
        self.atk = ATK()
        self.dmg_ratio = DMGMultiplier()
        self.resistance = ResistanceMutiplier()
        self.defense = DefenseMultiplier()
        self.critical = CriticalMultiplier()
        self.daze = DazeMultiplier()

        # attack
        self.skill = SkillMultiplier()

        # anomaly
        self.aa = AnomalyAttributeMultiplier()
        self.ap = AnomalyProficiencyMultiplier()
        self.anomaly_level = AnomalyLevelMultiplier()
        self.anomaly_acc = 0.0

        self.extras: list[ExtraMultiplier] = []

    def calc_anomaly(self):
        v = (
            self.atk.calc()
            * self.dmg_ratio.calc()
            * self.resistance.calc()
            * self.defense.calc()
            * self.daze.calc()
            # anomaly
            * self.aa.calc()
            * self.ap.calc()
            * self.anomaly_level.calc()
        ).value()

        for extra in self.extras:
            v *= extra.calc()

        return v

    def calc(self):
        v = (
            self.atk.calc()
            * self.dmg_ratio.calc()
            * self.resistance.calc()
            * self.defense.calc()
            * self.daze.calc()
            # normal
            * self.critical.calc()
            * self.skill.calc()
        ).value()
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
            self.resistance.add(-number)
        elif stat.kind == StatKind.STUN_DMG_RATIO:
            self.daze.add(number)
        elif stat.kind == StatKind.ANOMALY_PROFICIENCY:
            self.ap.add(number)

    def apply_agent_data(self, agent: AgentData):
        self.atk.agent = Number(agent.atk_base, "Agent basic ATK")
        self.defense.set_agent(agent.level)
        self.critical.ratio.add(Number(agent.crit_ratio, "Agent basic CRIT_RATIO"))
        self.critical.multi.add(Number(agent.crit_multi, "Agent basic CRIT_MULTI"))

        # anomaly
        self.ap.add(agent.anomaly_proficiency)
        self.anomaly_level.level = agent.level

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
        self.defense.set_enemy(b.enemy_level, b.enemy_base)
        self.aa.attribute = b.agent.attribute
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

    def show_normal(self):
        return (
            f"{self.atk} * {self.dmg_ratio} * {self.resistance} * {self.defense} * {self.daze}"
            + f" * {self.aa} * {self.ap} * {self.anomaly_level} = {self.calc()}"
        )

    def show_anomaly(self):
        return (
            f"{self.atk} * {self.dmg_ratio} * {self.resistance} * {self.defense} * {self.daze}"
            + f" * {self.critical}* {self.skill} = {self.calc_anomaly()} # acc={self.anomaly_acc}"
        )

    def __str__(self):
        return (
            f"{self.atk}             \t# base\n"
            + f"* {self.dmg_ratio} \t# dmg_ratio\n"
            + f"* {self.resistance}  \t# resistance\n"
            + f"* {self.defense}     \t# defense\n"
            + f"* {self.critical}    \t# critical\n"
            + f"* {self.daze}        \t# daze\n"
            + f"* {self.skill}       \t# skill\n"
            + f"= {self.calc()}"
        )


def calc_anomaly(dmgs):
    anomaly_dmgs = [(d.calc_anomaly(), d.anomaly_acc) for d in dmgs]
    total = sum(t[1] for t in anomaly_dmgs)
    result = 0.0
    s = "0.0"
    for value, acc in anomaly_dmgs:
        result += value * acc / total
        s += f" + {value} * {acc:.1f}/{total:.1f}"
    s += f" = {result:.1f}"
    return result, s


@dataclass
class ComboResult:
    total: float = 0.0
    dmgs: list[DMG] = field(default_factory=list)
    comment: str = ""
    anomaly_total: float = 0.0
    anomaly_detail: str = ""

    def __init__(self, total, dmgs: list[DMG], comment="", anomaly=False):
        self.total = total
        self.dmgs = dmgs
        self.comment = comment
        if anomaly:
            self.anomaly_total, self.anomaly_detail = calc_anomaly(self.dmgs)

    def show_normal(self):
        s = "\n".join([d.show_normal() for d in self.dmgs])
        s += f"\nIn Total : {self.total:.1f}; by {self.comment}"
        return s

    def show_anomaly(self):
        if not self.anomaly_total:
            self.anomaly_total, self.anomaly_detail = calc_anomaly(self.dmgs)

        s = "\n".join([d.show_anomaly() for d in self.dmgs])
        s += f"\nAcc calc: {self.anomaly_detail}"
        s += f"\nIn Total (anomaly) : {self.anomaly_total:.1f}; by {self.comment}"
        return s


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
        self.anomaly_dmgs = []
        self.final_anomaly_dmg = 0.0

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
            dmg.anomaly_acc = attack.anomaly
            self.dmgs.append(dmg)

        value = 0.0
        for dmg in self.dmgs:
            value += dmg.calc()
        return value

    def delta_analyze(self) -> list[ComboResult]:
        result = []
        base = self.calc()
        result.append(ComboResult(base, copy.deepcopy(self.dmgs), "Baseline"))

        def update_build(build, comment=""):
            new = self.calc(build, self.context)
            result.append(ComboResult(new, copy.deepcopy(self.dmgs), comment))

        def update_stat(extra):
            build = copy.copy(self.build).replace_extra(extra)
            new = self.calc(build, self.context)
            result.append(ComboResult(new, copy.deepcopy(self.dmgs), str(extra)))

        update_stat([StatValue(9, StatKind.PEN_FLAT)])
        update_stat([StatValue(19, StatKind.ATK_FLAT)])
        update_stat([StatValue(0.03, StatKind.ATK_RATIO)])
        update_stat([StatValue(0.03, StatKind.DMG_RATIO)])
        update_stat([StatValue(0.024, StatKind.CRIT_RATIO)])
        update_stat([StatValue(0.048, StatKind.CRIT_MULTI)])
        update_stat([StatValue(0.024, StatKind.PEN_RATIO)])
        update_stat([StatValue(9, StatKind.ANOMALY_PROFICIENCY)])

        disc4_stat = self.build.discs.at(4).primary
        if disc4_stat.kind == StatKind.CRIT_RATIO:
            update_stat(
                [
                    StatValue(-0.24, StatKind.CRIT_RATIO),
                    StatValue(+0.48, StatKind.CRIT_MULTI),
                ]
            )
        elif disc4_stat.kind == StatKind.CRIT_MULTI:
            update_stat(
                [
                    StatValue(+0.24, StatKind.CRIT_RATIO),
                    StatValue(-0.48, StatKind.CRIT_MULTI),
                ]
            )
        disc5_stat_neg = -self.build.discs.at(5).primary
        update_stat([disc5_stat_neg, StatValue(0.3, StatKind.ATK_RATIO)])
        update_stat([disc5_stat_neg, StatValue(0.3, StatKind.DMG_RATIO)])
        update_stat([disc5_stat_neg, StatValue(0.24, StatKind.PEN_RATIO)])

        if self.build.agent.level < 60:
            build = copy.deepcopy(self.build).update_agent_stats(level=60)
            update_build(build, "agent level -> 60")
        if self.build.weapon.level < 60:
            build = copy.deepcopy(self.build).update_weapon_level(level=60)
            update_build(build, "weapon level -> 60")
        if self.build.agent.skill_levels.core < 6:
            skill_levels = replace(
                self.build.agent.skill_levels,
                core=self.build.agent.skill_levels.core + 1,
            )
            build = copy.deepcopy(self.build).update_agent_stats(
                skill_levels=skill_levels
            )
            update_build(build, "core skill +1")
        if self.build.agent.skill_levels.basic < 16:
            skill_levels = replace(
                self.build.agent.skill_levels,
                basic=self.build.agent.skill_levels.basic + 1,
            )
            build = copy.deepcopy(self.build).update_agent_stats(
                skill_levels=skill_levels
            )
            update_build(build, "basic atk skill +1")

        return result

    def __str__(self):
        v = 0.0
        s = ""
        for dmg in self.dmgs:
            v += dmg.calc().value()
            s += str(dmg.show_normal())
            s += "\n"
        s += f"In total = {v}"
        return s


def print_combo_results(results: list[ComboResult], print_anomaly=False):
    base = results[0].total
    results[0].show_anomaly()
    anomaly_base = results[0].anomaly_total

    for r in results:
        ratio = (r.total / base - 1) * 100
        print(f"{r.show_normal()} ; delta ratio: {ratio:.3f}%\n")
        if print_anomaly:
            s = f"{r.show_anomaly()}"
            ratio = (r.anomaly_total / anomaly_base - 1) * 100
            s += f"; delta ratio: {ratio:.3f}%\n"
            print(s)
