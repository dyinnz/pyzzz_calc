from typing import Sequence

from pyzzz import dataset
from pyzzz.model import *
from pyzzz.agent import Agent
from pyzzz.hit import Hit, Attack


class AgentWithData(Agent):
    def __init__(
        self,
        name: str = "",
        level: int = 60,
        is_ascension: bool = False,
        repetition: int = 0,
        skill_levels: SkillLevels | None = None,
    ):
        super().__init__(name, level, is_ascension, repetition, skill_levels)

        if self.name:
            self._load_zzz_gg_data(self.name)

    def extra_multiplier(self) -> Sequence[ExtraMultiplier]:
        return []

    def load_cn_data(self, cn_name):
        self._skill = dataset.load_skills()[cn_name]

    def _load_zzz_gg_data(self, name: str):
        db = dataset.load_zzz_gg_agents()
        agent = db["agents"][name]
        self._camp = Camp.from_full_name(agent["CampName"])
        self._profession = Profession(agent["ProfessionName"].lower())
        self._attribute = Attribute(agent["ElementTypeName"].lower())

        self._growth.init.level = self.level
        self._growth.init.hp = agent["HpMax"]
        self._growth.hp_growth = agent["HPGrowth"] / 1e4
        self._growth.init.atk_base = agent["Atk"]
        self._growth.atk_growth = agent["AttackGrowth"] / 1e4
        self._growth.init.defense = agent["Def"]
        self._growth.defense_growth = agent["DefenceGrowth"] / 1e4
        self._growth.init.impact = agent["BreakStun"]
        self._growth.init.anomaly_master = agent["ElementMystery"]
        self._growth.init.energy_regen = agent["SpRecover"]
        self._growth.init.anomaly_proficiency = agent["ElementAbnormalPower"]

        ascension = db["ascensions"][name]
        for _, asc in ascension.items():
            self._ascensions.append(
                [
                    StatValue(asc["HpMax"], StatKind.HP_FLAT),
                    StatValue(asc["Atk"], StatKind.ATK_BASE),
                    StatValue(asc["Def"], StatKind.DEF_FLAT),
                ]
            )

        def parse_passive(m):
            result = []
            for k, v in m.items():
                if k == "ATK":
                    result.append(StatValue(v, StatKind.ATK_BASE))
                elif k == "Impact":
                    result.append(StatValue(v, StatKind.IMPACT))
                elif k == "CRIT Rate":
                    result.append(StatValue(v / 1e4, StatKind.CRIT_RATIO))
                elif k == "CRIT DMG":
                    result.append(StatValue(v / 1e4, StatKind.CRIT_MULTI))
                elif k == "Energy Regen":
                    result.append(StatValue(v, StatKind.ENERGY_REGEN))
                elif k == "Anomaly Mastery":
                    result.append(StatValue(v, StatKind.ANOMALY_MASTER))
                elif k == "Anomaly Proficiency":
                    result.append(StatValue(v, StatKind.ANOMALY_PROFICIENCY))
                elif k == "PEN Ratio":
                    result.append(StatValue(v, StatKind.PEN_RATIO))
                else:
                    raise Exception(f"unknown passive item {k} {v}")
            return result

        self._passives = [[]]
        passive = db["passives"][name]
        for p in passive.values():
            self._passives.append(parse_passive(p))

        self._fill_data()
