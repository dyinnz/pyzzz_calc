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


class Zhuyuan(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        repetition=0,
    ):
        name = "Zhu Yuan"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

    def core_skill1(self):
        def create():
            m = [0.20, 0.233, 0.266, 0.30, 0.333, 0.366, 0.40]
            return StatValue(m[self.skill_levels.core], StatKind.DMG_RATIO)

        return DynamicBuff(
            create,
            condition=HitContext(atk_kind=AttackKind.Basic),
            owner=self.name,
            source="core skill dmg ratio",
        )

    def core_skill2(self):
        def create():
            m = [0.20, 0.233, 0.266, 0.30, 0.333, 0.366, 0.40]
            return StatValue(m[self.skill_levels.core], StatKind.DMG_RATIO)

        return DynamicBuff(
            create,
            condition=HitContext(atk_kind=AttackKind.Basic),
            owner=self.name,
            source="core daze skill dmg ratio",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.30, StatKind.CRIT_RATIO),
            condition=HitContext(atk_attr=Attribute.All),
            owner=self.name,
            source="extra skill crit ratio",
        )

    def rep2(self):
        return StaticBuff(
            StatValue(0.50, StatKind.DMG_RATIO),
            condition=HitContext(atk_attr=Attribute.Ether),
            owner=self.name,
            source="ep2 Ether dmg ratio",
        )

    def rep4(self):
        return StaticBuff(
            StatValue(-0.25, StatKind.RES_RATIO),
            condition=HitContext(atk_attr=Attribute.Ether),
            owner=self.name,
            source="ep4 Ether res ratio",
        )

    def rep6(self):
        return StaticBuff(
            StatValue(8.8, StatKind.SKILL_MULTI),
            condition=HitContext(
                atk_attr=Attribute.Ether, atk_kind=AttackKind.SpecialEx
            ),
            owner=self.name,
            source="rep6 skill",
        )

    def buffs(self):
        res = [self.core_skill1(), self.core_skill2(), self.extra_skill()]
        if self._repetition >= 2:
            res.append(self.rep2())
        if self._repetition >= 4:
            res.append(self.rep4())
        # if context and context.agent == self.name and self._repetition >= 6:
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
