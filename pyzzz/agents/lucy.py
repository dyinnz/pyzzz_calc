from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.buff import DynamicBuff
from pyzzz.model import (
    SkillLevels,
    StatKind,
    StatValue,
)


class Lucy(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=6,
        **kw,
    ):
        name = "Lucy"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

    def atk_buff(self):
        def create():
            skill = self.skill_levels.special
            ratio = (13 + skill * 0.8) / 100
            flat = 40 + skill * 4
            if self.core_skill_atk is not None:
                value = self.core_skill_atk
            else:
                value = self.initial.atk * ratio + flat
            value = min(600, value)
            return StatValue(value, StatKind.ATK_FLAT)

        res = DynamicBuff(
            create,
            owner=self.name,
            source="core skill",
            for_team=True,
        )
        return res

    def buffs(self):
        return [self.atk_buff()]
