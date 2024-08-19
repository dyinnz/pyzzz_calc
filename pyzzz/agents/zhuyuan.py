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

class Zhuyuan(Agent):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=0,
    ):
        name = "Zhuyuan"
        Agent.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

        self.cn_name = "朱鸢"
        self.load_cn_data(self.cn_name)

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

        self.a1 = self._skill["普通攻击：请勿抵抗(以太)-一段"]
        self.a2 = self._skill["普通攻击：请勿抵抗(以太)-二段"]
        self.a3 = self._skill["普通攻击：请勿抵抗(以太)-三段"]

        self.e1 = self._skill["特殊技：鹿弹射击"]

        self.ex1 = self._skill["强化特殊技：全弹连射"]

        self.dash = self._skill["闪避反击：火力震爆-"]
        self.dogde = self._skill["闪避反击：火力震爆-"]
        self.chain = self._skill["连携技：歼灭模式-"]
        self.final = self._skill["终结技：歼灭模式MAX-"]

    def A1(self):
        value = self.a1["dmg"] + self.a1["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ether, value)

    def A2(self):
        value = self.a2["dmg"] + self.a2["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ether, value)

    def A3(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ether, value)

    def E1(self):
        value = self.e1["dmg"] + self.e1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Ether, value)

    def EX1(self):
        value = self.ex1["dmg"] + self.ex1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ether, value)
    
    def Dash(self):
        value = self.dash["dmg"] + self.dash["dmg_grow"] * (
            self.skill_levels.dogde - 1
        )
        return Attack(AttackKind.Dash, Attribute.Ether, value)

    def Dodge(self):
        value = self.dogde["dmg"] + self.dogde["dmg_grow"] * (
            self.skill_levels.dogde - 1
        )
        return Attack(AttackKind.Dodge, Attribute.Ether, value)
    
    def Chain(self):
        value = self.chain["dmg"] + self.chain["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Ether, value)

    def Final(self):
        value = self.final["dmg"] + self.final["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Final, Attribute.Ether, value)

    def core_skill1(self):
        def create():
            m = [0.20, 0.233, 0.266, 0.30, 0.333, 0.366, 0.40]
            return StatValue(m[self.skill_levels.core], StatKind.DMG_RATIO)

        return DynamicBuff(
            create,
            condition=ContextData(atk_kind=AttackKind.Basic),
            source="Zhuyuan core skill dmg ratio")
    
    def core_skill2(self):
        def create():
            m = [0.20, 0.233, 0.266, 0.30, 0.333, 0.366, 0.40]
            return StatValue(m[self.skill_levels.core], StatKind.DMG_RATIO)
        
        return DynamicBuff(
            create,
            condition=ContextData(atk_kind=AttackKind.Basic),
            source="Zhuyuan core daze skill dmg ratio")
        

    def extra_skill(self):
        return Buff(
            StatValue(0.30, StatKind.CRIT_RATIO),
            condition=ContextData(atk_attr=Attribute.All),
            source="Zhuyuan extra skill crit ratio",
        )

    def rep2(self):
        return Buff(
            StatValue(0.50, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.Ether),
            source="Zhuyuan ep2 Ether dmg ratio",
        )
    
    def rep4(self):
        return Buff(
            StatValue(-0.25, StatKind.RES_RATIO),
            condition=ContextData(atk_attr=Attribute.Ether),
            source="Zhuyuan ep4 Ether res ratio",
        )

    def rep6(self):
        return Buff(
            StatValue(2.2, StatKind.SKILL_MULTI),
            condition=ContextData(atk_attr=Attribute.Ether, atk_kind=AttackKind.SpecialEx),
            source="Zhuyuan rep6 skill",
        )

    def buffs(self, _: bool = True):
        res = [self.core_skill(), self.extra_skill()]
        if self._repetition >= 2:
            res.append(self.rep2())
        if self._repetition >= 4:
            res.append(self.rep4())
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
