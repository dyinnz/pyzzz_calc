from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.buff import StaticBuff
from pyzzz.model import (
    SkillLevels,
    StatKind,
    StatValue,
)


class Piper(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        repetition=6,
        **kw,
    ):
        name = "Piper"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

    def rep2_buff(self):
        return StaticBuff(
            StatValue(0.2, StatKind.DMG_RATIO),
            owner=self.name,
            source="rep2 buff",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.18, StatKind.DMG_RATIO),
            owner=self.name,
            source="core skill dmg ratio",
            for_team=True,
        )

    def buffs(self):
        return [self.rep2_buff(), self.extra_skill()]
