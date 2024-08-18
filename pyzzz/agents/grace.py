from pyzzz.agents.agent import Agent
from pyzzz.buff import Buff, DynamicBuff
from pyzzz.model import *


class GraceExtraMultiplier(ExtraMultiplier):

    def active(self, anomaly: bool, context: ContextData):
        return anomaly

    def calc(self):
        return 1 + 0.36

    def show(self):
        return "(1 + 0.36)"


class Grace(Agent):

    def __init__(
        self, level=60, skill_levels: SkillLevels | None = None, repetition=0, **kw
    ):
        name = "Grace"
        Agent.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw
        )

        self.cn_name = "格莉丝"
        self.load_cn_data(self.cn_name)

        self.a1 = self._skill["普通攻击：高压射钉-一段"]
        self.a2 = self._skill["普通攻击：高压射钉-二段"]
        self.a3 = self._skill["普通攻击：高压射钉-三段"]
        self.a3 = self._skill["普通攻击：高压射钉-三段"]
        self.a4 = self._skill["普通攻击：高压射钉-四段"]
        self.ax = self._skill["普通攻击：高压射钉-垫步射击"]

        self.e = self._skill["特殊技：工程清障-"]
        self.ex = self._skill["强化特殊技：超规工程清障-单个手雷"]

        self.chain = self._skill["连携技：协作施工-"]
        self.final = self._skill["终结技：工程爆破请勿接近-"]

    def A1(self):
        value = self.a1["dmg"] + self.a1["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, 0)

    def A2(self):
        value = self.a2["dmg"] + self.a2["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, 0)

    def A31(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value * 0.4, 0)

    def A32(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(
            AttackKind.Basic, Attribute.Electric, value * 0.6, self.a3["anomaly"] * 0.6
        )

    def E(self):
        value = self.e["dmg"] + self.e["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Electric, value, self.e["anomaly"])

    def EX(self):
        value = self.ex["dmg"] + self.ex["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Electric, value, self.ex["anomaly"])

    def Chain(self):
        value = self.chain["dmg"] + self.chain["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(
            AttackKind.Chain, Attribute.Electric, value, self.chain["anomaly"]
        )

    def Final(self):
        value = self.final["dmg"] + self.final["dmg_grow"] * (
            self.skill_levels.final - 1
        )
        return Attack(
            AttackKind.Final, Attribute.Electric, value, self.final["anomaly"]
        )

    def extra_multiplier(self):
        return [GraceExtraMultiplier()]
