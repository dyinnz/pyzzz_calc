from pyzzz.model import *

from typing import Sequence
from pyzzz.buff import *
from pyzzz.enemy import Enemy
from pyzzz.agent import Agent
from pyzzz.hit import Hit
from pyzzz.multiplier import *
from pyzzz.model import *


class HitDMG:
    def __init__(self, hit: Hit, agent: Agent, enemy: Enemy):
        self._hit = hit
        self._agent = agent
        self._enemy = enemy
        self._context = HitContext.default()

        self._active_buffs = list[Buff]()

        # common multiplier
        self.dmg_ratio = DMGMultiplier()
        self.resistance = ResistanceMutiplier()
        self.defense = DefenseMultiplier()
        self.daze = DazeMultiplier()

        # attack multiplier
        self.critical = CriticalMultiplier()
        self.skill = SkillMultiplier([])
        self.atk = ATKMultiplier()

        # anomaly multiplier
        self.aa = AnomalyAttributeMultiplier()
        self.ap = AnomalyProficiencyMultiplier()
        self.anomaly_level = AnomalyLevelMultiplier()
        self.anomaly_acc = 0.0

        # extra multiplier
        self.extras: Sequence[ExtraMultiplier] = []

        # cache the result
        self.common_result = 0.0
        self.normal_result = 0.0
        self.anomaly_result = 0.0

    def fill_context(self):
        self._context.agent = self._agent.name
        self._context.atk_kind = self._hit.kind
        self._context.atk_attr = self._hit.attribute
        self._context.daze = self._enemy.daze

    def fill_data(self):
        self.dmg_ratio.add(self._agent.static.dmg_ratio)
        self.defense.set_agent(self._agent.level)
        self.defense.set_enemy(self._enemy.level, self._enemy.defense_base)
        self.defense.pen_ratio.add(self._agent.static.pen_ratio)
        self.defense.pen_flat.add(self._agent.static.pen_flat)
        if self._enemy.daze:
            self.daze.add(0.5)

        self.critical.ratio.add(self._agent.static.crit_ratio)
        self.critical.multi.add(self._agent.static.crit_multi)
        self.skill.add(self._hit.multi)
        self.atk.agent = Number(self._agent.static.atk_base)
        self.atk.weapon = Number(self._agent.static.atk_weapon)
        self.atk.static_ratio.add(self._agent.static.atk_ratio)
        self.atk.static_flat.add(self._agent.static.atk_flat)

        self.aa.attribute = self._hit.attribute
        self.ap.add(self._agent.static.anomaly_proficiency)
        self.anomaly_level.level = self._enemy.level
        self.anomaly_acc = self._hit.anomaly

    def apply_stat(self, stat: StatValue):
        number = Number(stat.value)
        if stat.kind == StatKind.ATK_RATIO:
            self.atk.dynamic_ratio.add(number)
        elif stat.kind == StatKind.ATK_FLAT:
            self.atk.dynamic_flat.add(number)
        elif stat.kind == StatKind.CRIT_RATIO:
            self.critical.ratio.add(number)
        elif stat.kind == StatKind.CRIT_MULTI:
            self.critical.multi.add(number)
        elif stat.kind == StatKind.PEN_RATIO:
            self.defense.pen_ratio.add(number)
        elif stat.kind == StatKind.PEN_FLAT:
            self.defense.pen_flat.add(number)
        elif stat.kind == StatKind.ENEMY_DEF_RATIO:
            self.defense.enemy_def_ratio.add(number)
        elif stat.kind == StatKind.DMG_RATIO:
            self.dmg_ratio.add(number)
        elif stat.kind == StatKind.RES_RATIO:
            self.resistance.add(-number)
        elif stat.kind == StatKind.STUN_DMG_RATIO:
            self.daze.add(number)
        elif stat.kind == StatKind.ANOMALY_PROFICIENCY:
            self.ap.add(number)
        elif stat.kind == StatKind.SKILL_MULTI:
            self.skill.add(number)

    def apply_buff(self):
        for buf in self._active_buffs:
            stat = buf.produce(self._context)  # TODO:
            self.apply_stat(stat)

    def calc_common(self):
        if self.common_result == 0.0:
            self.common_result = (
                Number(1)
                * self.dmg_ratio.calc()
                * self.resistance.calc()
                * self.defense.calc()
                * self.daze.calc()
            )
        return self.common_result

    def calc_normal(self):
        if self.normal_result == 0.0:
            v = (
                Number(self.calc_common())
                * self.critical.calc()
                * self.skill.calc()
                * self.atk.calc()
            ).value()
            for extra in self.extras:
                if extra.active(False, self._context):
                    v *= extra.calc()
            self.normal_result = v
        return self.normal_result

    def calc_anomaly(self):
        if self.anomaly_result == 0.0:
            v = (
                Number(self.calc_common())
                # anomaly
                * self.aa.calc()
                * self.ap.calc()
                * self.anomaly_level.calc()
                * self.atk.calc()
            ).value()

            for extra in self.extras:
                if extra.active(True, self._context):
                    v *= extra.calc()
            self.anomaly_result = v
        return self.anomaly_result

    def show_common(self):
        return f"{self.dmg_ratio} * {self.resistance} * {self.defense} * {self.daze}"

    def show_normal(self):
        s = f"{self.show_common()} * {self.critical}* {self.skill} * {self.atk}"
        for extra in self.extras:
            if extra.active(True, self._context):
                s += f" * {extra.show()}"
        s += f" = {self.calc_normal():.1f}\t# acc={self.anomaly_acc}"
        return s

    def show_anomaly(self):
        s = f"{self.show_common()} * {self.aa} * {self.ap} * {self.anomaly_level} * {self.atk}"
        for extra in self.extras:
            if extra.active(False, self._context):
                s += f" * {extra.show()}"
        s += f" = {self.calc_anomaly():.1f}"
        return s


class ComboDMG:
    def __init__(self):
        self.dmgs = list[HitDMG]()
        self.anomaly_multiplier: list[ExtraMultiplier] = []
        self.comment = ""

    def calc_normal(self):
        total = 0.0
        for dmg in self.dmgs:
            total += dmg.calc_normal()
        return total

    def show_normal(self, base=0.0):
        total = self.calc_normal()
        s = "\n".join((d.show_normal() for d in self.dmgs))
        if base == 0.0:
            s += f"\nNormal DMG : {total:.1f}; by {self.comment}\n"
        else:
            s += f"\nNormal DMG : {total:.1f}; delta {(total/base - 1)*100:.3f}%; by {self.comment}\n"
        return s

    def calc_anomaly(self):
        anomaly_dmgs = [(d.calc_anomaly(), d.anomaly_acc) for d in self.dmgs]
        total_acc = sum(t[1] for t in anomaly_dmgs)
        result = 0.0
        for value, acc in anomaly_dmgs:
            result += value * acc / total_acc
        for multi in self.anomaly_multiplier:
            result *= multi.calc()
        return result

    def show_anomaly(self, base=0.0):
        total = self.calc_anomaly()
        total_acc = sum((d.anomaly_acc for d in self.dmgs))

        s = "\n".join(
            (
                f"{d.show_anomaly()}\t# pct={d.anomaly_acc/total_acc * 100:.1f}%" ""
                for d in self.dmgs
            )
        )
        for multi in self.anomaly_multiplier:
            s += f"\n* {multi.show()}"

        if base == 0.0:
            s += f"\nAnomaly DMG : {total:.1f}; by {self.comment}\n"
        else:
            s += f"\nAnomaly DMG : {total:.1f}; delta {(total/base - 1)*100:.3f}%; by {self.comment}\n"
        return s

    def set_comment(self, c: str):
        self.comment = c
        return self
