from pyzzz.agents.agent import Agent
from pyzzz.buff import Buff, DynamicBuff
from pyzzz.model import (
    AgentData,
    Attack,
    AttackKind,
    Attribute,
    ContextData,
    SkillLevels,
    StatKind,
    StatValue,
)

class Rina(Agent):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=0,
    ):
        name = "Rina"
        Agent.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

        self.cn_name = "丽娜"
        self.load_cn_data(self.cn_name)

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

        self.a1 = self._skill["普通攻击：痛打呆子-一段"]
        self.a2 = self._skill["普通攻击：痛打呆子-二段"]
        self.a3 = self._skill["普通攻击：痛打呆子-三段"]
        self.a4 = self._skill["普通攻击：痛打呆子-四段"]

        self.e1 = self._skill["特殊技：砸扁笨蛋-"]

        self.ex1 = self._skill["强化特殊技：笨蛋消失魔法-"]

        self.dogde = self._skill["闪避反击：邦布回魂-"]
        self.chain = self._skill["连携技：侍者守则-"]
        self.final = self._skill["终结技：女王的侍从们-"]

    def A1(self):
        value = self.a1["dmg"] + self.a1["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value)

    def A2(self):
        value = self.a2["dmg"] + self.a2["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value)

    def A3(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Electric, value)
    
    def A4(self):
        value = self.a4["dmg"] + self.a4["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Electric, value)

    def E1(self):
        value = self.e1["dmg"] + self.e1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Electric, value)

    def EX1(self):
        value = self.ex1["dmg"] + self.ex1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Electric, value)

    def Dodge(self):
        value = self.dogde["dmg"] + self.dogde["dmg_grow"] * (
            self.skill_levels.dogde - 1
        )
        return Attack(AttackKind.Dodge, Attribute.Electric, value)

    def Chain(self):
        value = self.chain["dmg"] + self.chain["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Electric, value)

    def Final(self):
        value = self.final["dmg"] + self.final["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Final, Attribute.Electric, value)

    def core_skill(self):
        def create():
            m = [6, 7.5, 9, 10.2, 10.8, 11.4, 12]
            value = self.static.pen_ratio() * 0.25 + m
            value = min(30, value)
            return StatValue(value[self.skill_levels.core], StatKind.PEN_RATIO)

        return DynamicBuff(
            create,
            source="Rina core skill pen ratio",
        )

    def extra_skill(self):
        return Buff(
            StatValue(0.1, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.Electric),
            source="Rina extra skill Electric dmg ratio",
        )

    def rep1(self):
        def create():
            m = [6, 7.5, 9, 10.2, 10.8, 11.4, 12]
            value = self.static.pen_ratio() * 0.25 + m
            value = min(30, value)*0.3
            return StatValue(value[self.skill_levels.core], StatKind.PEN_RATIO)

        return DynamicBuff(
            create,
            source="Rina ep1 pen ratio",
        )
    
    def rep2(self):
        return Buff(
            StatValue(0.15, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.All, atk_kind=AttackKind.All),
            source="Rina rep2 dmg ratio",
        )


    def rep6(self):
        return Buff(
            StatValue(0.15, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.Electric, atk_kind=AttackKind.All),
            source="Rina rep6 Electric dmg ratio",
        )

    def buffs(self, _: bool = True):
        res = [self.core_skill(), self.extra_skill()]
        if self._repetition >= 1:
            res.append(self.rep1())
        if self._repetition >= 2:
            res.append(self.rep2())
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
