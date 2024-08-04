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


class Soukaku(Agent):
    def __init__(
        self, level=60, skill_levels: Optional[SkillLevels] = None, core_skill_atk=1000
    ):
        Agent.__init__(self, skill_levels=skill_levels)

        self.name = "Soukaku"
        self.cn_name = "苍角"
        self.load_cn_data(self.cn_name)

        self.core_skill_atk = core_skill_atk

    def core_skill(self):
        return Buff(
            StatValue(self.core_skill_atk, StatKind.ATK_FLAT),
            source="Soukaku core skill atk dynamic flat",
        )

    def extra_skill(self):
        return Buff(
            StatValue(0.2, StatKind.DMG_RATIO),
            condition=ContextData(atk_attr=Attribute.Ice),
            source="Soukaku extra skill ice ratio",
        )

    def buffs(self):
        return [self.core_skill(), self.extra_skill()]
