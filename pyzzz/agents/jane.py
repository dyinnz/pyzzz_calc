from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.model import *
from pyzzz.buff import DynamicBuff
from pyzzz.hit import Attack


class JaneExtraMultiplier(ExtraMultiplier):
    def __init__(self, agent: AgentWithData):
        self.agent = agent

    @property
    def crit_ratio(self):
        return min(0.4 + 0.0016 * self.agent.static.anomaly_proficiency, 1.0)

    def active(self, anomaly: bool, context: HitContext):
        return anomaly

    def calc(self):
        return 1 + self.crit_ratio * 0.5

    def show(self):
        return f"(1 + {self.crit_ratio:.4f} * 0.5) # Jane anomaly extra criti multiplier"


class Jane(AgentWithData):
    def __init__(
        self,
        level=60,
        is_ascension=False,
        skill_levels: SkillLevels | None = None,
        repetition=0,
        **kw,
    ):
        name = "Jane"
        super().__init__(
            name=name,
            level=level,
            is_ascension=is_ascension,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

        self._cn_name = "简"
        self.load_cn_data(self._cn_name)

        self.a1 = self._skill["普通攻击：跳步刃舞-一段"]
        self.a2 = self._skill["普通攻击：跳步刃舞-二段"]
        self.a3 = self._skill["普通攻击：跳步刃舞-三段"]
        self.a4 = self._skill["普通攻击：跳步刃舞-四段"]
        self.a5 = self._skill["普通攻击：跳步刃舞-五段"]
        self.a6 = self._skill["普通攻击：跳步刃舞-六段"]
        self.ax = self._skill["普通攻击：萨霍夫跳-连续攻击"]
        self.ay = self._skill["普通攻击：萨霍夫跳-终结一击"]

        self.e = self._skill["特殊技：掠空-"]
        self.ex = self._skill["强化特殊技：掠空-横扫-"]

        self.dash1 = self._skill["冲刺攻击：刀刃跳-一段"]
        self.dash2 = self._skill["冲刺攻击：刀刃跳-二段"]
        self.dash3 = self._skill["冲刺攻击：虚像突刺-"]
        self.dodge1 = self._skill["闪避反击：疾影-一段"]
        self.dodge2 = self._skill["闪避反击：疾影-二段"]
        self.dodge3 = self._skill["闪避反击：疾影连舞-"]

        self.chain = self._skill["连携技：罪孽生花-"]
        self.final = self._skill["终结技：终幕演出-"]

    def A1(self):
        value = self.a1["dmg"] + self.a1["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, self.a1["anomaly"])

    def A2(self):
        value = self.a2["dmg"] + self.a2["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, self.a2["anomaly"])

    def A3(self):
        value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, self.a3["anomaly"])

    def A4(self):
        value = self.a4["dmg"] + self.a4["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, self.a4["anomaly"])

    def A5(self):
        value = self.a5["dmg"] + self.a5["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, self.a5["anomaly"])

    def A6(self):
        value = self.a6["dmg"] + self.a6["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, self.a6["anomaly"])

    def AX(self):
        value = self.ax["dmg"] + self.ax["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, self.ax["anomaly"])

    def AY(self):
        value = self.ay["dmg"] + self.ay["dmg_grow"] * (self.skill_levels.basic - 1)
        return Attack(AttackKind.Basic, Attribute.Physical, value, self.ay["anomaly"])

    def E(self):
        value = self.e["dmg"] + self.e["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Physical, value, self.e["anomaly"])

    def EX(self):
        value = self.ex["dmg"] + self.ex["dmg_grow"] * (self.skill_levels.special - 1)
        return Attack(AttackKind.Special, Attribute.Physical, value, self.ex["anomaly"])

    def Dodge1(self):
        value = self.dodge1["dmg"] + self.dodge1["dmg_grow"] * (
            self.skill_levels.dodge - 1
        )
        return Attack(
            AttackKind.Special, Attribute.Physical, value, self.dodge1["anomaly"]
        )

    def Dodge2(self):
        value = self.dodge2["dmg"] + self.dodge2["dmg_grow"] * (
            self.skill_levels.dodge - 1
        )
        return Attack(
            AttackKind.Special, Attribute.Physical, value, self.dodge2["anomaly"]
        )

    def Dodge3(self):
        value = self.dodge3["dmg"] + self.dodge3["dmg_grow"] * (
            self.skill_levels.dodge - 1
        )
        return Attack(
            AttackKind.Special, Attribute.Physical, value, self.dodge3["anomaly"]
        )

    def passion_stream(self):
        def create():
            value = min((self.static.anomaly_proficiency - 120) * 2, 600)
            return StatValue(value, StatKind.ATK_FLAT)

        return DynamicBuff(
            create,
            source=f"{self.name} passion stream atk",
        )

    def buffs(self):
        return [self.passion_stream()]

    def extra_multiplier(self):
        return [JaneExtraMultiplier(self)]
