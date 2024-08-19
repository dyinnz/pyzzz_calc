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

class Soldier11(Agent):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=0,
    ):
        name = "Soldier11"
        Agent.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

        self.cn_name = "11号"
        self.load_cn_data(self.cn_name)

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

        self.a1 = self._skill["普通攻击：火力镇压-一段"]
        self.a2 = self._skill["普通攻击：火力镇压-二段"]
        self.a3 = self._skill["普通攻击：火力镇压-三段"]
        self.a4 = self._skill["普通攻击：火力镇压-四段"]

        self.e1 = self._skill["特殊技：烈火"]

        self.ex1 = self._skill["强化特殊技：盛燃烈火"]

        self.dash = self._skill["冲刺攻击：火力镇压-"]
        self.dogde = self._skill["闪避反击：逆火-"]

        self.chain = self._skill["连携技：昂扬烈焰-"]
        self.final = self._skill["终结技：轰鸣烈焰-"]

    def A1(self):
        value = self.a1["dmg"] + self.a1["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Fire, value)

    def A2(self):
        value = self.a2["dmg"] + self.a2["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Fire, value)

    def A3(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Fire, value)
    
    def A4(self):
        value = self.a4["dmg"] + self.a4["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Fire, value)

    def E1(self):
        value = self.e1["dmg"] + self.e1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Fire, value)

    def EX1(self):
        value = self.ex1["dmg"] + self.ex1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Fire, value)

    def Dash(self):
        value = self.dash["dmg"] + self.dash["dmg_grow"] * (
            self.skill_levels.dogde - 1
        )
        return Attack(AttackKind.Dash, Attribute.Fire, value)
    
    def Dodge(self):
        value = self.dogde["dmg"] + self.dogde["dmg_grow"] * (
            self.skill_levels.dogde - 1
        )
        return Attack(AttackKind.Dodge, Attribute.Fire, value)

    def Chain(self):
        value = self.chain["dmg"] + self.chain["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Fire, value)

    def Final(self):
        value = self.final["dmg"] + self.final["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Final, Attribute.Fire, value)

    def core_skill(self):
        def create():
            m = [0.35, 0.408, 0.466, 0.525, 0.583, 0.641, 0.70]
            return StatValue(m[self.skill_levels.core], StatKind.DMG_RATIO)

        return DynamicBuff(
            create,
            source="Soldier11 core skill dmg ratio",
        )


    def extra_skill(self):
        return( Buff(
            StatValue(0.1, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.Fire),
            source="Soldier11 extra skill dmg ratio",
        ),
            Buff(
            StatValue(0.225, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.Fire),
            source="Soldier11 extra skill daze fire dmg ratio",
        ))
    
    def rep2(self):
        return Buff(
            StatValue(0.36, StatKind.DMG_RATIO),
            condition=[ContextData(atk_kind=AttackKind.Basic),
                       ContextData(atk_kind=AttackKind.Dash),
                       ContextData(atk_kind=AttackKind.Dodge)],
            source="Soldier11 ep2 Physical res ratio",
        )

    def rep6(self):
        return Buff(
            StatValue(-0.25, StatKind.RES_RATIO),
            condition=[ContextData(atk_attr=Attribute.Fire, atk_kind=AttackKind.Basic),
                       ContextData(atk_attr=Attribute.Fire, atk_kind=AttackKind.Dash)],
            source="Soldier11 rep6 Fire res ratio",
        )

    def buffs(self, _: bool = True):
        res = [self.core_skill(), self.extra_skill()]
        if self._repetition >= 2:
            res.append(self.rep2())
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
