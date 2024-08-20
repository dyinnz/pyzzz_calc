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

class Nicole(Agent):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=0,
    ):
        name = "Nicole"
        Agent.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

        self.cn_name = "妮可"
        self.load_cn_data(self.cn_name)

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

        self.e1 = self._skill["特殊技：糖衣炮弹-A"]
        self.e2 = self._skill["特殊技：糖衣炮弹-B"]

        self.ex1 = self._skill["强化特殊技：夹心糖衣炮弹-蓄力"]
        self.ex2 = self._skill["强化特殊技：夹心糖衣炮弹-炮击A"]
        self.ex3 = self._skill["强化特殊技：夹心糖衣炮弹-炮击B"]
        self.ex4 = self._skill["强化特殊技：夹心糖衣炮弹-能量场"]

        self.dogde1 = self._skill["闪避反击：牵制炮击-A"]
        self.dogde2 = self._skill["闪避反击：牵制炮击-B"]

        self.chain1 = self._skill["连携技：高价以太爆弹-炮击A"]
        self.chain2 = self._skill["连携技：高价以太爆弹-炮击B"]
        self.chain3 = self._skill["连携技：高价以太爆弹-能量场"]
        self.final1 = self._skill["终结技：特制以太榴弹-炮击"]
        self.final2 = self._skill["终结技：特制以太榴弹-能量场"]

    def E1(self):
        value = self.e1["dmg"] + self.e1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Ether, value)

    def E2(self):
        value = self.e2["dmg"] + self.e2["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Ether, value)


    def EX1(self):
        value = self.ex1["dmg"] + self.ex1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ether, value)
    
    def EX2(self):
        value = self.ex2["dmg"] + self.ex2["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ether, value)

    def EX3(self):
        value = self.ex3["dmg"] + self.ex3["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ether, value)

    def EX4(self):
        value = self.ex4["dmg"] + self.ex4["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ether, value)


    def Dodge1(self):
        value = self.dogde1["dmg"] + self.dogde1["dmg_grow"] * (
            self.skill_levels.dodge - 1
        )
        return Attack(AttackKind.Dodge, Attribute.Ether, value)

    def Dodge2(self):
        value = self.dogde2["dmg"] + self.dogde2["dmg_grow"] * (
            self.skill_levels.dodge - 1
        )
        return Attack(AttackKind.Dodge, Attribute.Ether, value)


    def Chain1(self):
        value = self.chain1["dmg"] + self.chain1["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Ether, value)

    def Chain2(self):
        value = self.chain2["dmg"] + self.chain2["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Ether, value)

    def Chain3(self):
        value = self.chain3["dmg"] + self.chain3["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Ether, value)


    def Final1(self):
        value = self.final1["dmg"] + self.final1["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Final, Attribute.Ether, value)

    def Final2(self):
        value = self.final2["dmg"] + self.final2["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Final, Attribute.Ether, value)


    def core_skill(self):
        def create():
            m = [0.2, 0.25, 0.30, 0.34, 0.36, 0.38, 0.40][self.skill_levels.core]
            return StatValue(m, StatKind.DEF_RES)

        return DynamicBuff(
            create,
            source="Nicole core skill def res",
        )

    def extra_skill(self):
        return Buff(
            StatValue(0.25, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.Ether, atk_kind=AttackKind.All),
            source="Nicole extra skill Ether dmg ratio",
        )


    def rep6(self):
        return Buff(
            StatValue(0.15, StatKind.CRIT_RATIO),
            condition=ContextData(atk_attr=Attribute.All, atk_kind=AttackKind.All),
            source="Nicole rep6 crit ratio",
        )


    def buffs(self, context: ContextData | None = None):
        res = [self.core_skill(), self.extra_skill()]
        # if context and context.agent == self.name and self._repetition >= 6:
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
