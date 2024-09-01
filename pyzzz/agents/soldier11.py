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


class Soldier11(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        repetition=0,
    ):
        name = "Soldier 11"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

        self._cn_name = "「11号」"
        self.load_cn_data(self.cn_name)

    def core_skill(self):
        def create():
            m = [0.35, 0.408, 0.466, 0.525, 0.583, 0.641, 0.70]
            return StatValue(m[self.skill_levels.core], StatKind.DMG_RATIO)

        return DynamicBuff(
            create,
            source="Soldier11 core skill dmg ratio",
        )

    def extra_skill(self):
        return (
            StaticBuff(
                StatValue(0.1, StatKind.DMG_RATIO),
                condition=HitContext(atk_attr=Attribute.Fire),
                source="Soldier11 extra skill dmg ratio",
            ),
            StaticBuff(
                StatValue(0.225, StatKind.DMG_RATIO),
                condition=HitContext(atk_attr=Attribute.Fire),
                source="Soldier11 extra skill daze fire dmg ratio",
            ),
        )

    def rep2(self):
        return StaticBuff(
            StatValue(0.36, StatKind.DMG_RATIO),
            condition=[
                HitContext(atk_kind=AttackKind.Basic),
                HitContext(atk_kind=AttackKind.Dash),
                HitContext(atk_kind=AttackKind.Dodge),
            ],
            source="Soldier11 ep2 Physical res ratio",
        )

    def rep6(self):
        return StaticBuff(
            StatValue(-0.25, StatKind.RES_RATIO),
            condition=[
                HitContext(atk_attr=Attribute.Fire, atk_kind=AttackKind.Basic),
                HitContext(atk_attr=Attribute.Fire, atk_kind=AttackKind.Dash),
            ],
            source="Soldier11 rep6 Fire res ratio",
        )

    def buffs(self):
        res = [self.core_skill(), self.extra_skill()]
        if self._repetition >= 2:
            res.append(self.rep2())
        # if context and context.agent == self.name and self._repetition >= 6:
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
