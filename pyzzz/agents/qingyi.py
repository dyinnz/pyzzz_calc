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
from pyzzz.hit import Attack


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

        self._cn_name = "青衣"
        self.load_cn_data(self._cn_name)

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

        self.a1 = self._skill["普通攻击：一煞-一段"]
        self.a2 = self._skill["普通攻击：一煞-二段"]
        self.a3 = self._skill["普通攻击：一煞-三段"]
        self.a4 = self._skill["普通攻击：一煞-四段"]
        self.a5 = self._skill["普通攻击:一煞-四段(强化)"]
        self.a6 = self._skill["普通攻击:醉花月云转-突进攻击"]
        self.a7 = self._skill["普通攻击:醉花月云转-终结一击"]

        self.e1 = self._skill["特殊技：昼锦堂"]

        self.ex1 = self._skill["强化特殊技：月上海棠"]

        self.dogde = self._skill["闪避反击：意不尽-"]
        self.chain = self._skill["连携技：太平令-"]
        self.final = self._skill["终结技：八声甘州-"]

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

    def A5(self):
        value = self.a5["dmg"] + self.a5["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Electric, value)

    def A6(self):
        value = self.a6["dmg"] + self.a6["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Electric, value)

    def A7(self):
        value = self.a7["dmg"] + self.a7["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Electric, value)

    def E1(self):
        value = self.e1["dmg"] + self.e1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Electric, value)

    def EX1(self):
        value = self.ex1["dmg"] + self.ex1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Electric, value)

    def Dodge(self):
        value = self.dogde["dmg"] + self.dogde["dmg_grow"] * (
            self.skill_levels.dodge - 1
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
            m0 = [0.02, 0.024, 0.027, 0.03, 0.034, 0.037, 0.04][self.skill_levels.core]
            m = m0 * 20
            return StatValue(m, StatKind.STUN_DMG_RATIO)

        return DynamicBuff(
            create,
            source="Qingyi core skill stun dmg ratio",
        )

    def extra_skill(self):
        m = max((self.static.impact - 120) * 6, 0)
        return StaticBuff(
            StatValue(m, StatKind.ATK_FLAT),
            source="Qingyi extra skill atk flat",
        )

    def rep1(self):
        return (
            Buff(
                StatValue(-0.15, StatKind.ENEMY_DEF_RATIO),
                condition=HitContext(atk_attr=Attribute.Physical),
                source="Qingyi ep1 def res",
            ),
            StaticBuff(
                StatValue(0.2, StatKind.CRIT_RATIO),
                condition=HitContext(atk_attr=Attribute.Physical),
                source="Qingyi ep1 crit ratio",
            ),
        )

    def rep2(self):
        def create():
            m0 = [0.02, 0.024, 0.027, 0.03, 0.034, 0.037, 0.04][self.skill_levels.core]
            m = m0 * 20 * 0.35
            return StatValue(m, StatKind.STUN_DMG_RATIO)

        return DynamicBuff(
            create,
            source="Qingyi ep2 stun dmg ratio",
        )

    def rep6(self):
        return StaticBuff(
            StatValue(0.2, StatKind.RES_RATIO),
            condition=HitContext(atk_attr=Attribute.All, atk_kind=AttackKind.All),
            source="Qingyi rep6 res ratio",
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
