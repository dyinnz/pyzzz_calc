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

from pyzzz.hit import Hit, Attack


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

        self._cn_name = "艾莲"
        self.load_cn_data(self._cn_name)

        self.a1 = self._skill["普通攻击：急冻修剪法-一段"]
        self.a2 = self._skill["普通攻击：急冻修剪法-二段"]
        self.a3 = self._skill["普通攻击：急冻修剪法-三段"]
        self.ex1 = self._skill["强化特殊技：横扫-"]
        self.ex2 = self._skill["强化特殊技：鲨卷风-"]
        self.chain = self._skill["连携技：雪崩-"]
        self.f = self._skill["终结技：永冬狂宴-"]

    def A1(self):
        value = self.a1["dmg"] + self.a1["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ice, value, self.a1["anomaly"])

    def A2(self):
        value = self.a2["dmg"] + self.a2["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ice, value, self.a2["anomaly"])

    def A3(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ice, value, self.a3["anomaly"])

    def EX1(self):
        value = self.ex1["dmg"] + self.ex1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ice, value, self.ex1["anomaly"])

    def EX2(self):
        value = self.ex2["dmg"] + self.ex2["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ice, value, self.ex2["anomaly"])

    def Chain(self):
        value = self.chain["dmg"] + self.chain["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Ice, value, self.chain["anomaly"])

    def Final(self):
        value = self.f["dmg"] + self.f["dmg_grow"] * (self.skill_levels.chain - 1)
        return Attack(AttackKind.Final, Attribute.Ice, value, self.f["anomaly"])

    def core_skill(self):
        def create():
            multi = [0.50, 0.583, 0.66, 0.75, 0.8333, 0.916, 1]
            return StatValue(multi[self.skill_levels.core], StatKind.CRIT_MULTI)

        return DynamicBuff(
            create,
            condition=HitContext(atk_kind=AttackKind.Basic),
            source="Ellen core skill criti multi",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.3, StatKind.DMG_RATIO), source="Ellen extra skill ice ratio"
        )

    def buffs(self):
        return [self.core_skill(), self.extra_skill()]
