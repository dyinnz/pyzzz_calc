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


class Soukaku(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=6,
        **kw,
    ):
        name = "Soukaku"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

        self._cn_name = "苍角"
        self.load_cn_data(self._cn_name)

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

        self.a1 = self._skill["普通攻击：打年糕（霜染刃旗）-一段"]
        self.a2 = self._skill["普通攻击：打年糕（霜染刃旗）-二段"]
        self.a3 = self._skill["普通攻击：打年糕（霜染刃旗）-三段"]

        self.e1 = self._skill["特殊技：吹凉便当-一段"]
        self.e2 = self._skill["特殊技：吹凉便当-终结段"]

        self.ex1 = self._skill["强化特殊技：扇走蚊虫-风场"]
        self.ex2 = self._skill["强化特殊技：扇走蚊虫-连续攻击"]

        self.ey1 = self._skill["特殊技：集合啦！-展旗"]
        self.ey2 = self._skill["特殊技：集合啦！-快速展旗"]
        self.ey3 = self._skill["特殊技：集合啦！-收旗攻击"]

        self.dogde = self._skill["闪避反击：别抢零食-"]
        self.dash = self._skill["冲刺攻击：对半分（霜染刃旗）-"]
        self.chain = self._skill["连携技：鹅鸡斩-"]
        self.final = self._skill["终结技：大份鹅鸡斩-"]

    def A1(self):
        value = self.a1["dmg"] + self.a1["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ice, value, self.a1["anomaly"])

    def A2(self):
        value = self.a2["dmg"] + self.a2["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ice, value, self.a2["anomaly"])

    def A3(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Ice, value, self.a3["anomaly"])

    def E1(self):
        value = self.e1["dmg"] + self.e1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Ice, value, self.e1["anomaly"])

    def E2(self):
        value = self.e2["dmg"] + self.e2["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Ice, value, self.e2["anomaly"])

    def EX1(self):
        value = self.ex1["dmg"] + self.ex1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ice, value, self.ex1["anomaly"])

    def EX2(self):
        value = self.ex2["dmg"] + self.ex2["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.SpecialEx, Attribute.Ice, value, self.ex2["anomaly"])

    def EY1(self):
        value = self.ey1["dmg"] + self.ey1["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Ice, value, self.ey1["anomaly"])

    def EY2(self):
        value = self.ey1["dmg"] + self.ey2["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Ice, value, self.ey2["anomaly"])

    def EY3(self):
        value = self.ey3["dmg"] + self.ey3["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Ice, value, self.ey3["anomaly"])

    def Dodge(self):
        value = self.dogde["dmg"] + self.dogde["dmg_grow"] * (
            self.skill_levels.dodge - 1
        )
        return Attack(AttackKind.Dodge, Attribute.Ice, value, self.dogde["anomaly"])

    def Dash(self):
        value = self.dash["dmg"] + self.dash["dmg_grow"] * (self.skill_levels.dodge - 1)
        return Attack(AttackKind.Dash, Attribute.Ice, value, self.dash["anomaly"])

    def Chain(self):
        value = self.chain["dmg"] + self.chain["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Chain, Attribute.Ice, value, self.chain["anomaly"])

    def Final(self):
        value = self.final["dmg"] + self.final["dmg_grow"] * (
            self.skill_levels.chain - 1
        )
        return Attack(AttackKind.Final, Attribute.Ice, value, self.final["anomaly"])

    def final_buff(self):
        return StaticBuff(
            StatValue(0.15, StatKind.CRIT_RATIO),
            condition=[
                HitContext(atk_kind=AttackKind.Final, agent=self.name),
                HitContext(atk_kind=AttackKind.Basic, agent=self.name),
                HitContext(atk_kind=AttackKind.Dash, agent=self.name),
            ],
            source=f"{self.name} final buff +15% critical ratio",
        )

    def core_skill(self):
        def create():
            m = [0, 12.5, 15, 17, 18, 19, 20][self.skill_levels.core] / 100 * 2
            value = (
                self.core_skill_atk
                if self.core_skill_atk is not None
                else self.static.static_atk() * m
            )
            value = min(1000, value)
            return StatValue(value, StatKind.ATK_FLAT)

        return DynamicBuff(
            create,
            source="Soukaku core skill atk dynamic flat",
            for_team=True,
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.2, StatKind.DMG_RATIO),
            condition=HitContext(atk_attr=Attribute.Ice),
            source="Soukaku extra skill ice dmg ratio",
            for_team=True,
        )

    def rep4(self):
        return StaticBuff(
            StatValue(-0.1, StatKind.RES_RATIO),
            condition=HitContext(atk_attr=Attribute.Ice),
            source="Soukaku rep4 ice res ratio",
            for_team=True,
        )

    def rep6(self):
        return StaticBuff(
            StatValue(0.45, StatKind.DMG_RATIO),
            condition=[
                HitContext(
                    agent=self.name, atk_attr=Attribute.Ice, atk_kind=AttackKind.Basic
                ),
                HitContext(
                    agent=self.name, atk_attr=Attribute.Ice, atk_kind=AttackKind.Dash
                ),
            ],
            source="Soukaku rep6 ice dmg ratio",
        )

    def buffs(self):
        res = [self.core_skill(), self.extra_skill(), self.final_buff()]
        if self._repetition >= 4:
            res.append(self.rep4())
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
