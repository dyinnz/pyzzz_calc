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


class Nekomata(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        repetition=0,
    ):
        name = "Nekomata"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

    def core_skill(self):
        def create():
            m = [0.3, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
            return StatValue(m[self.skill_levels.core], StatKind.DMG_RATIO)

        return DynamicBuff(
            create,
            owner=self.name,
            source="core skill dmg ratio",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.35, StatKind.DMG_RATIO),
            condition=HitContext(atk_attr=Attribute.All, atk_kind=AttackKind.SpecialEx),
            owner=self.name,
            source="extra skill SpecialEx dmg ratio",
        )

    def rep1(self):
        return StaticBuff(
            StatValue(-0.16, StatKind.RES_RATIO),
            condition=HitContext(atk_attr=Attribute.Physical),
            owner=self.name,
            source="rep1 res ratio",
        )

    def rep4(self):
        return StaticBuff(
            StatValue(0.14, StatKind.CRIT_RATIO),
            condition=HitContext(atk_attr=Attribute.All),
            owner=self.name,
            source="rep4 crit ratio",
        )

    def rep6(self):
        return StaticBuff(
            StatValue(0.54, StatKind.CRIT_MULTI),
            condition=HitContext(atk_attr=Attribute.All, atk_kind=AttackKind.All),
            owner=self.name,
            source="rep6 crit multi",
        )

    def buffs(self):
        res = [self.core_skill(), self.extra_skill()]
        if self._repetition >= 1:
            res.append(self.rep1())
        if self._repetition >= 4:
            res.append(self.rep4())
        # if context and context.agent == self.name and self._repetition >= 6:
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
