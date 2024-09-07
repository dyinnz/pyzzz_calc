import typing
from pyzzz.env import Env
import dataclasses

from pyzzz.dmg import ComboDMG
from pyzzz.model import *


class DeltaAnalyzer:
    def __init__(self, env: Env, combo: t.Sequence[str]):
        self._env = env
        self._combo = combo

    def base(self):
        return self._env.calc_combo(self._combo, "Baseline")

    def update_stat(self, extras: list[StatValue], idx=0):
        env = self._env.clone()
        env.agent(idx).set_equipment(static=extras)
        return env.calc_combo(self._combo, str(extras))

    def quick(self) -> list[ComboDMG]:
        r = []

        def update(extras):
            r.append(self.update_stat(extras))

        r.append(self.base())
        update([StatValue(9, StatKind.PEN_FLAT)])
        update([StatValue(19, StatKind.ATK_FLAT)])
        update([StatValue(0.03, StatKind.ATK_RATIO)])
        update([StatValue(0.03, StatKind.DMG_RATIO)])
        update([StatValue(0.024, StatKind.CRIT_RATIO)])
        update([StatValue(0.048, StatKind.CRIT_MULTI)])
        update([StatValue(0.024, StatKind.PEN_RATIO)])
        update([StatValue(9, StatKind.ANOMALY_PROFICIENCY)])
        # update([StatValue(90, StatKind.ANOMALY_PROFICIENCY)])

        agent0 = self._env.agent(0)

        disc4_stat = agent0.discs.at(4).primary
        if disc4_stat.kind == StatKind.CRIT_RATIO:
            update(
                [
                    StatValue(-0.24, StatKind.CRIT_RATIO),
                    StatValue(+0.48, StatKind.CRIT_MULTI),
                ]
            )
        else:
            update(
                [
                    StatValue(+0.24, StatKind.CRIT_RATIO),
                    StatValue(-0.48, StatKind.CRIT_MULTI),
                ]
            )
        disc5_stat = agent0.discs.at(5).primary
        if disc5_stat != StatValue(0.3, StatKind.ATK_RATIO):
            update([-disc5_stat, StatValue(0.3, StatKind.ATK_RATIO)])
        if disc5_stat != StatValue(0.3, StatKind.DMG_RATIO):
            update([-disc5_stat, StatValue(0.3, StatKind.DMG_RATIO)])
        if disc5_stat != StatValue(0.3, StatKind.PEN_RATIO):
            update([-disc5_stat, StatValue(0.24, StatKind.PEN_RATIO)])
        update(
            [
                -disc5_stat,
                -agent0.discs.suit2_stats[0],
                StatValue(0.32, StatKind.PEN_RATIO),
            ]
        )

        if agent0.level < 60:
            env = self._env.clone()
            env.agent(0).set_stats(level=60)
            r.append(env.calc_combo(self._combo, "Agent Level -> 60"))

        if agent0.weapon.level < 60:
            env = self._env.clone()
            env.agent(0).set_stats(level=60)
            r.append(env.calc_combo(self._combo, "Weapon Level -> 60"))

        if agent0.skill_levels.core < 6:
            env = self._env.clone()
            skill_levels = dataclasses.replace(
                agent0.skill_levels, core=agent0.skill_levels.core + 1
            )
            env.agent(0).set_stats(skill_levels=skill_levels)
            r.append(env.calc_combo(self._combo, "Core Skill +1"))

        if agent0.skill_levels.basic < 16:
            env = self._env.clone()
            skill_levels = dataclasses.replace(
                agent0.skill_levels, basic=agent0.skill_levels.basic + 1
            )
            env.agent(0).set_stats(skill_levels=skill_levels)
            r.append(env.calc_combo(self._combo, "Basic Skill +1"))

        return r
