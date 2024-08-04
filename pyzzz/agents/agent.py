from typing import Optional
import copy

from pyzzz import dataset
from pyzzz.buff import Buff
from pyzzz.model import AgentData, SkillLevels


class Agent:
    def __init__(self, skill_levels: Optional[SkillLevels] = None):
        self.skill_levels: SkillLevels = skill_levels if skill_levels else SkillLevels()
        self.data: AgentData = AgentData()
        self.origin_data = copy.deepcopy(self.data)
        self.skill = {}

    def load_cn_data(self, cn_name):
        self.data: AgentData = dataset.load_agents_basic()[cn_name]
        self.skill = dataset.load_skills()[cn_name]

    def buffs(self) -> list[Buff]:
        return []
