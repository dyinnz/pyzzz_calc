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

class Nekomata(Agent):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=0,
    ):
        name = "Nekomata"
        Agent.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
        )

        self.cn_name = "猫又"
        self.load_cn_data(self.cn_name)

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

        self.a1 = self._skill["普通攻击：猫猫爪刺-一段"]
        self.a2 = self._skill["普通攻击：猫猫爪刺-二段"]
        self.a3 = self._skill["普通攻击：猫猫爪刺-三段"]
        self.a4 = self._skill["普通攻击：猫猫爪刺-四段"]
        self.a5 = self._skill["普通攻击：猫猫爪刺-五段"]
        self.a6 = self._skill["普通攻击：赤色之刃"]

        self.e1 = self._skill["特殊技：奇袭"]

        self.ex1 = self._skill["强化特殊技：超~凶奇袭"]

        self.dogde = self._skill["闪避反击：虚影双刺-"]
        self.chain = self._skill["连携技：刃爪挥击-"]
        self.final = self._skill["终结技：刃爪强袭-"]

    def A1(self):
        value = self.a1["dmg"] + self.a1["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value)

    def A2(self):
        value = self.a2["dmg"] + self.a2["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value)

    def A3(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value)
    
    def A4(self):
        value = self.a4["dmg"] + self.a4["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value)
    
    def A5(self):
        value = self.a5["dmg"] + self.a5["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value)
    
    def A6(self):
        value = self.a6["dmg"] + self.a6["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value)

    def E1(self):
        value = self.e1["dmg"] + self.e1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Physical, value)

    def EX1(self):
        value = self.ex1["dmg"] + self.ex1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Physical, value)

    def Dodge(self):
        value = self.dogde["dmg"] + self.dogde["dmg_grow"] * (
            self.skill_levels.dogde - 1
        )
        return Attack(AttackKind.Dodge, Attribute.Physical, value)

    def Chain(self):
        value = self.chain["dmg"] + self.chain["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Physical, value)

    def Final(self):
        value = self.final["dmg"] + self.final["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Final, Attribute.Physical, value)

    def core_skill(self):
        def create():
            m = [0.3, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
            return StatValue(m[self.skill_levels.core], StatKind.DMG_RATIO)

        return DynamicBuff(
            create,
            source="Nekomata core skill dmg ratio",
        )

    def extra_skill(self):
        return Buff(
            StatValue(0.35, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.All, atk_kind=AttackKind.SpecialEx),
            source="Nekomata extra skill SpecialEx dmg ratio",
        )

    def rep1(self):
        return Buff(
            StatValue(-0.16, StatKind.RES_RATIO),
            condition=ContextData(atk_attr=Attribute.Physical),
            source="Nekomata ep1 res ratio",
        )
    def rep4(self):
        return Buff(
            StatValue(0.14, StatKind.CRIT_RATIO),
            condition=ContextData(atk_attr=Attribute.All),
            source="Nekomata ep4 crit ratio",
        )


    def rep6(self):
        return Buff(
            StatValue(0.54, StatKind.CRIT_MULTI),
            condition=ContextData(atk_attr=Attribute.All, atk_kind=AttackKind.All),
            source="Nekomata rep6 crit multi",
        )

    def buffs(self, _: bool = True):
        res = [self.core_skill(), self.extra_skill()]
        if self._repetition >= 1:
            res.append(self.rep1())
        if self._repetition >= 4:
            res.append(self.rep4())
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
