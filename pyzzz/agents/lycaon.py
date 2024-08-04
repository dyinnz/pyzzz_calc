from typing import Optional

from pyzzz import dataset
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
    def __init__(self, level=60, skill_levels: Optional[SkillLevels] = None):
        Agent.__init__(self, skill_levels=skill_levels)

        self.name = "Lycaon"
        self.cn_name = "莱卡恩"
        self.load_cn_data(self.cn_name)

    def core_skill(self):
        return Buff(
            StatValue(-0.25, StatKind.RES_RATIO),
            condition=ContextData(atk_attr=Attribute.Ice),
            source=f"{self.name} core skill Ice DMG RES",
        )

    def extra_skill(self):
        return Buff(
            StatValue(0.35, StatKind.STUN_DMG_RATIO),
            condition=ContextData(daze=True),
            source=f"{self.name} extra skill Stun DMG Multiplier",
        )

    def buffs(self):
        return [self.core_skill(), self.extra_skill()]
