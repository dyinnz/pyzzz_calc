from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.buff import StaticBuff, DynamicBuff
from pyzzz.model import (
    AttackKind,
    HitContext,
    SkillLevels,
    StatKind,
    StatValue,
)


class Ellen(AgentWithData):
    def __init__(
        self, level=60, skill_levels: SkillLevels | None = None, repetition=0, **kw
    ):
        name = "Ellen"
        super().__init__(
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

    def core_skill(self):
        def create():
            multi = [0.50, 0.583, 0.66, 0.75, 0.8333, 0.916, 1]
            return StatValue(multi[self.skill_levels.core], StatKind.CRIT_MULTI)

        return DynamicBuff(
            create,
            condition=HitContext(atk_kind=AttackKind.Basic),
            owner=self.name,
            source="core skill - basic-atk",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.3, StatKind.DMG_RATIO),
            owner=self.name,
            source="extra skill",
        )

    def buffs(self):
        return [self.core_skill(), self.extra_skill()]
