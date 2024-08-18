from pyzzz.agents.agent import Agent
from pyzzz.buff import Buff
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


class Lycaon(Agent):
    def __init__(
        self, level=60, skill_levels: SkillLevels | None = None, repetition=0, **kw
    ):
        name = "Lycaon"
        Agent.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

        self.cn_name = "莱卡恩"
        self.load_cn_data(self.cn_name)

        self.chain = self._skill["连携技：遵命-"]

    def Chain(self):
        value = self.chain["dmg"] + self.chain["dmg_grow"] * (
            self.skill_levels.special - 1
        )
        return Attack(AttackKind.Chain, Attribute.Ice, value)

    def core_skill(self):
        return Buff(
            StatValue(-0.25, StatKind.RES_RATIO),
            condition=ContextData(atk_attr=Attribute.Ice),
            source=f"{self._name} core skill Ice DMG RES",
        )

    def extra_skill(self):
        return Buff(
            StatValue(0.35, StatKind.STUN_DMG_RATIO),
            condition=ContextData(daze=True),
            source=f"{self._name} extra skill Stun DMG Multiplier",
        )

    def buffs(self, _: bool = True):
        return [self.core_skill(), self.extra_skill()]
