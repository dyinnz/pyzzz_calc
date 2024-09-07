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


class Rina(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        repetition=0,
    ):
        name = "Rina"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

    def core_skill(self):
        def create():
            m = [0.06, 0.075, 0.09, 0.102, 0.108, 0.114, 0.12][self.skill_levels.core]
            value = self.initial.pen_ratio * 0.25 + m
            value = min(0.3, value)
            return StatValue(value, StatKind.PEN_RATIO)

        return DynamicBuff(
            create,
            owner=self.name,
            source="core skill pen ratio",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.1, StatKind.DMG_RATIO),
            condition=HitContext(atk_attr=Attribute.Electric),
            owner=self.name,
            source="extra skill Electric dmg ratio",
        )

    def rep1(self):
        def create():
            m = [0.06, 0.075, 0.09, 0.102, 0.108, 0.114, 0.12][self.skill_levels.core]
            value = self.initial.pen_ratio * 0.25 + m
            value = min(0.3, value) * 0.3
            return StatValue(value, StatKind.PEN_RATIO)

        return DynamicBuff(
            create,
            owner=self.name,
            source="ep1 pen ratio",
        )

    def rep2(self):
        return StaticBuff(
            StatValue(0.15, StatKind.DMG_RATIO),
            condition=HitContext(atk_attr=Attribute.All, atk_kind=AttackKind.All),
            owner=self.name,
            source="rep2 dmg ratio",
        )

    def rep6(self):
        return StaticBuff(
            StatValue(0.15, StatKind.DMG_RATIO),
            condition=HitContext(atk_attr=Attribute.Electric, atk_kind=AttackKind.All),
            owner=self.name,
            source="rep6 Electric dmg ratio",
        )

    def buffs(self):
        res = [self.core_skill(), self.extra_skill()]
        if self._repetition >= 1:
            res.append(self.rep1())
        if self._repetition >= 2:
            res.append(self.rep2())
        # if context and context.agent == self.name and self._repetition >= 6:
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
