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


class Qingyi(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=0,
    ):
        name = "Qingyi"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

    def core_skill(self):
        def create():
            m0 = [0.02, 0.024, 0.027, 0.03, 0.034, 0.037, 0.04][self.skill_levels.core]
            m = m0 * 20
            return StatValue(m, StatKind.STUN_DMG_RATIO)

        return DynamicBuff(
            create,
            owner=self.name,
            source="core skill stun dmg ratio",
        )

    def extra_skill(self):
        m = max((self.initial.impact - 120) * 6, 0)
        return StaticBuff(
            StatValue(m, StatKind.ATK_FLAT),
            owner=self.name,
            source="extra skill atk flat",
        )

    def rep1(self):
        return (
            StaticBuff(
                StatValue(-0.15, StatKind.DEF_REDUCE),
                condition=HitContext(atk_attr=Attribute.Physical),
                owner=self.name,
                source="ep1 def res",
            ),
            StaticBuff(
                StatValue(0.2, StatKind.CRIT_RATIO),
                condition=HitContext(atk_attr=Attribute.Physical),
                owner=self.name,
                source="ep1 crit ratio",
            ),
        )

    def rep2(self):
        def create():
            m0 = [0.02, 0.024, 0.027, 0.03, 0.034, 0.037, 0.04][self.skill_levels.core]
            m = m0 * 20 * 0.35
            return StatValue(m, StatKind.STUN_DMG_RATIO)

        return DynamicBuff(
            create,
            owner=self.name,
            source="ep2 stun dmg ratio",
        )

    def rep6(self):
        return StaticBuff(
            StatValue(0.2, StatKind.ATTR_RES),
            condition=HitContext(atk_attr=Attribute.All, atk_kind=AttackKind.All),
            owner=self.name,
            source="rep6 res ratio",
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
