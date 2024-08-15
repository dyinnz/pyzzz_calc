import copy
import itertools
import math

from pyzzz import dataset
from pyzzz.buff import Buff
from pyzzz.model import *


class Agent:
    def __init__(
        self,
        name="",
        level=60,
        is_ascension=False,
        skill_levels: SkillLevels | None = None,
        repetition=0,
    ):
        # from dataset
        self._camp = ""
        self._profession = Profession.All
        self._attribute = Attribute.All
        self._growth = AgentDataWithGrowth()
        self._ascensions: list[list[StatValue]] = []
        self._passives: list[list[StatValue]] = []
        self._skill = {}

        # from user input
        self._name = name
        self._level = level
        self._is_ascension = is_ascension
        self._skill_levels: SkillLevels = (
            skill_levels if skill_levels else SkillLevels()
        )
        self._repetition = repetition

        # final stats board
        self._base = AgentData()  # init + growth + weapon base
        self._static = AgentData()  # base + weapon primary + discs
        self._weapon = WeaponData(0, 0, StatValue.create_empty())

        if name:
            self.load_zzz_gg_data(name)
            self.fill_base()

    @property
    def name(self):
        return self._name

    @property
    def camp(self):
        return self._camp

    @property
    def profession(self):
        return self._profession

    @property
    def attribute(self):
        return self._attribute

    @property
    def level(self):
        return self._level

    @property
    def is_ascension(self):
        return self._is_ascension

    @property
    def skill_levels(self):
        return self._skill_levels

    @property
    def base(self):
        return self._base

    @property
    def static(self):
        if not self._static:
            raise Exception("logical error : static stats shall be re-calc")
        return self._static

    # after user inputs changed, this method shall be called
    def fill_base(self):
        self._base = copy.deepcopy(self._growth.init)
        self._base.level = self.level
        self._base.hp += math.floor(self._growth.hp_growth * (self.level - 1))
        self._base.defense += math.floor(self._growth.defense_growth * (self.level - 1))
        self._base.atk_base += math.floor(self._growth.atk_growth * (self.level - 1))
        # remember set weapon atk again
        self._base.atk_weapon = self._weapon.atk

        if not self._ascensions:
            raise Exception("expected ascension data")
        if not self._passives:
            raise Exception("expected ascension data")

        asc_rank = (self.level - 1) // 10 + int(
            self.level % 10 == 0 and self.is_ascension
        )

        stats = itertools.chain(
            self._ascensions[asc_rank], self._passives[self.skill_levels.core]
        )
        for stat in stats:
            self._base.apply_stat(stat)
        self._static = AgentData()  # clear static

    def apply_base_changes(self, changes: AgentData):
        self._base = self._base + changes
        self._static = AgentData()  # clear static
        return self

    def set_weapon(self, weapon: WeaponData):
        self._weapon = weapon
        self._base.atk_weapon = weapon.atk
        self._static = AgentData()  # clear static
        return self

    def calc_static(self, discs: DiscGroup, extra: list[StatValue] | None = None):
        self._static = copy.deepcopy(self._base)
        self._static.apply_stat(self._weapon.primary)
        for s in discs.suit2_stats:
            self._static.apply_stat(s)
        for d in discs.discs:
            self._static.apply_stat(d.primary)
            for s in d.secondaries:
                self._static.apply_stat(s)
        if extra:
            for s in extra:
                self._static.apply_stat(s)
        return self

    @staticmethod
    def _with_filled(func):
        def _with_filled_wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            self.fill_base()
            return res

        return _with_filled_wrapper

    @_with_filled
    def set_stats(self, level=None, is_ascension=None, skill_levels=None):
        if level is not None:
            self._level = level
        if is_ascension is not None:
            self._is_ascension = is_ascension
        if skill_levels is not None:
            self._skill_levels = skill_levels
        return self

    def buffs(self, _: bool = True) -> list[Buff]:
        return []

    def __str__(self):
        return f"{self._name} - {self._camp}/{self._profession}/{self._attribute}\n{self._growth}\n{self._ascensions}\n{self._passives}\n{self._static}"

    def load_cn_data(self, cn_name):
        # self.data: AgentData = dataset.load_agents_basic()[cn_name]
        self._skill = dataset.load_skills()[cn_name]

    def load_zzz_gg_data(self, name: str):

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
        self._growth.init.attribte_master = agent["ElementMystery"]
        self._growth.init.energy_regen = agent["SpRecover"]
        self._growth.init.anomaiy_proficiency = agent["ElementAbnormalPower"]

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
                    result.append(StatValue(v, StatKind.ANOMALY))
                elif k == "PEN Ratio":
                    result.append(StatValue(v, StatKind.PEN_RATIO))
                else:
                    raise Exception(f"unknown passive item {k} {v}")
            return result

        self._passives = [[]]
        passive = db["passives"][name]
        for p in passive.values():
            self._passives.append(parse_passive(p))
