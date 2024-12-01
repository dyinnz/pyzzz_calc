from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.buff import StaticBuff, DynamicBuff
from pyzzz.model import (
    AttackKind,
    Attribute,
    HitContext,
    SkillLevels,
    StatKind,
    StatValue,
)


class Nicole(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        repetition=0,
    ):
        name = "Nicole"
        super().__init__(
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

    def core_skill(self):
        def create():
            m = [0.2, 0.25, 0.30, 0.34, 0.36, 0.38, 0.40][self.skill_levels.core]
            return StatValue(m, StatKind.DEF_REDUCE)

        return DynamicBuff(
            create,
            owner=self.name,
            source="core skill def res",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.25, StatKind.DMG_RATIO),
            condition=HitContext(atk_attr=Attribute.Ether, atk_kind=AttackKind.All),
            owner=self.name,
            source="extra skill Ether dmg ratio",
        )

    def rep6(self):
        return StaticBuff(
            StatValue(0.15, StatKind.CRIT_RATIO),
            condition=HitContext(atk_attr=Attribute.All, atk_kind=AttackKind.All),
            owner=self.name,
            source="rep6 crit ratio",
        )

    def buffs(self):
        res = [self.core_skill(), self.extra_skill()]
        # if context and context.agent == self.name and self._repetition >= 6:
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
