import copy
import dataclasses
from pyzzz.buff import *
from pyzzz.enemy import Enemy
from pyzzz.agent import Agent
from pyzzz import agents, weapons
from pyzzz.multiplier import *
from pyzzz.model import *
from pyzzz.build import FullBuild
from pyzzz.dmg import *


class Env:
    def __init__(self):
        self._agents = [Agent(), Agent(), Agent()]

        self._enemy = Enemy()

        self._buffs: list[dict[str, BuffBase]] = [{}, {}, {}]
        self._team_buffs: dict[str, BuffBase] = {}

    def agent(self, i: int) -> Agent:
        return self._agents[i]

    def set_agent(self, i: int, agent: Agent):
        self._agents[i] = agent

    @property
    def captain(self) -> Agent:
        return self._agents[0]

    @property
    def agents(self):
        return self._agents

    @property
    def enemy(self):
        return self._enemy

    def clone(self) -> "Env":
        env = Env()
        env._agents = copy.deepcopy(self._agents)
        env._agents = copy.deepcopy(self._agents)
        return env

    def reset_static(self):
        # Reset all states to static which dynamic buff shall be reset
        self._buffs = [{}, {}, {}]
        self._team_buffs.clear()
        for i, agent in enumerate(self.agents):
            for b in agent.all_buffs():
                if b.for_team:
                    self._team_buffs[b.source] = b
                else:
                    self._buffs[i][b.source] = b

    def debug_str(self):
        pass

    def calc_combo(self, combo, comment="") -> ComboDMG:
        self.reset_static()

        result = ComboDMG()

        for hit in combo:
            dmg = HitDMG()
            dmg._hit = hit(self.agent(0))
            dmg._agent = self.agent(0)  # TODO
            dmg._enemy = self._enemy
            dmg.fill_context()
            dmg.fill_data()
            for b in self._buffs[0].values():
                dmg._active_buffs.append(b)
            for b in self._team_buffs.values():
                dmg._active_buffs.append(b)
            dmg.fill_buff()
            result.dmgs.append(dmg)

        result.comment = comment
        return result

    def __str__(self):
        self.reset_static()
        s = ""
        for agent in self._agents:
            if agent.name:
                s += f"{agent}\n"
        s += "Buffs:\n"
        for buff in self._team_buffs.values():
            s += f"\tteam - {buff}\n"
        for i, agent_buffs in enumerate(self._buffs):
            for buff in agent_buffs.values():
                s += f"\tagent#{i+1} - {buff}\n"
        return s

    @staticmethod
    def from_full(data: FullBuild):
        env = Env()
        weapon = weapons.create_weapon(
            data.weapon_name, level=data.weapon_level, repetition=data.weapon_rep
        )

        discs = data.discs
        discs.generate_suits()

        kw = dict(
            level=data.agent_level,
            skill_levels=data.skill_levels,
            repetition=data.agent_rep,
        )
        if data.agent_asc:
            kw["is_ascension"] = data.agent_asc
        agent = agents.create_agent(
            data.agent_name,
            **kw,
        )
        agent.set_equipment(weapon, discs)

        env.set_agent(0, agent)

        # XXX: refactor me
        i = 1
        for name, kw in data.team.items():
            a = agents.create_agent(name, **kw)
            env.set_agent(i, a)
            i += 1

        env._enemy = Enemy(level=data.enemy_level, defense_base=data.enemy_base)

        return env


class DeltaAnalyzer:
    def __init__(self, env: Env, combo: list):
        self._env = env
        self._combo = combo

    def base(self):
        return self._env.calc_combo(self._combo, "Baseline")

    def update_stat(self, extras: list[StatValue], idx=0):
        env = self._env.clone()
        env.agent(idx).set_equipment(extras=extras)
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
        disc5_stat_neg = -agent0.discs.at(5).primary
        update([disc5_stat_neg, StatValue(0.3, StatKind.ATK_RATIO)])
        update([disc5_stat_neg, StatValue(0.3, StatKind.DMG_RATIO)])
        update([disc5_stat_neg, StatValue(0.24, StatKind.PEN_RATIO)])

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
            r.append(env.calc_combo(self._combo, "Core Skill -> 60"))

        if agent0.skill_levels.basic < 6:
            env = self._env.clone()
            skill_levels = dataclasses.replace(
                agent0.skill_levels, basic=agent0.skill_levels.basic + 1
            )
            env.agent(0).set_stats(skill_levels=skill_levels)
            r.append(env.calc_combo(self._combo, "Basic Skill -> 60"))

        return r
