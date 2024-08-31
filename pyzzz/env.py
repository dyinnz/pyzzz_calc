import copy

from pyzzz import agents, weapons
from pyzzz.agent import Agent
from pyzzz.build import FullBuild
from pyzzz.dmg import HitDMG, ComboDMG
from pyzzz.enemy import Enemy
from pyzzz.buff import Buff
from pyzzz.model import *
from pyzzz.multiplier import *

from typing import Sequence


class Env:
    def __init__(self):
        self._agents = [Agent(), Agent(), Agent()]

        self._enemy = Enemy()

        self._buffs: list[dict[str, Buff]] = [{}, {}, {}]
        self._team_buffs: dict[str, Buff] = {}

        self._disable_buffs: set[str] = set()

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
        env._disable_buffs = copy.deepcopy(self._disable_buffs)
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

    def disable(self, buf: str):
        self._disable_buffs.add(buf)

    def calc_combo(self, combo: Sequence, comment="") -> ComboDMG:
        self.reset_static()

        result = ComboDMG()

        for hit in combo:
            dmg = HitDMG(hit(self.agent(0)), self.agent(0), self._enemy)
            dmg.name = hit.__qualname__
            dmg.fill_context()
            dmg.fill_data()
            # TODO: refactor me
            for b in self._buffs[0].values():
                if b.source not in self._disable_buffs:
                    dmg._active_buffs.append(b)
            for b in self._team_buffs.values():
                if b.source not in self._disable_buffs:
                    dmg._active_buffs.append(b)
            dmg.apply_buff()
            result.dmgs.append(dmg)

        for multi in self.agent(0).extra_multiplier():
            if multi.active(True, HitContext()):
                result.anomaly_multiplier.append(multi)

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

    @staticmethod
    def from_agent_build(data: AgentBuild):
        weapon = weapons.create_weapon(
            data.weapon_name, level=data.weapon_level, repetition=data.weapon_rep
        )

        discs = data.discs
        discs.generate_suits()
        kw = dict(
            level=data.agent_level,
            skill_levels=data.skills,
            repetition=data.agent_rep,
        )
        agent = agents.create_agent(
            data.agent_name,
            **kw,
        )
        agent.set_equipment(weapon, discs)
        return agent

    @staticmethod
    def from_input(data: CalcInput):
        env = Env()

        if data.agent1.agent_name:
            env.set_agent(0, Env.from_agent_build(data.agent1))
        if data.agent2.agent_name:
            env.set_agent(1, Env.from_agent_build(data.agent2))
        if data.agent3.agent_name:
            env.set_agent(2, Env.from_agent_build(data.agent3))
        env._enemy = Enemy(level=data.enemy.level, defense_base=data.enemy.base)

        return env
