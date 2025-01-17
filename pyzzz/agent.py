from typing import Sequence
import math
import abc
import copy
import itertools
from pyzzz.model import *
from pyzzz.buff import Buff
from pyzzz.weapon import Weapon
from pyzzz.discs import get_suit4_buff
from pyzzz.hit import GenerateHit


class Agent:
    def __init__(
        self,
        name: str = "",
        level: int = 60,
        is_ascension: bool = False,
        repetition: int = 0,
        skill_levels: SkillLevels | None = None,
    ):
        # from user input
        self._name = name
        self._level = level
        self._is_ascension = is_ascension
        self._repetition = repetition
        self._skill_levels: SkillLevels = (
            SkillLevels() if skill_levels is None else skill_levels
        )
        self._cn_name = ""

        # from dataset
        self._camp = ""
        self._profession = Profession.All
        self._attribute = Attribute.All
        self._growth = AgentGrowthStats()
        self._ascensions: list[list[StatValue]] = []  # level -> [stats]
        self._passives: list[list[StatValue]] = []  # level -> [stats]
        self._skill = {}

        # basic : lazy repr { init + growth }
        self._basic = AgentStats()
        # static : lazy repr { basic * (1 + ratio) + flat }
        self._static = AgentStats()
        # dynamic : lazy repr { static * (1 + ratio) + flat }
        self._dynamic = AgentStats()

        # calc-ed static
        self._initial = AgentValueStats()
        # calc-ed dynamic
        self._final = AgentValueStats()

        self._weapon = Weapon()
        self._discs = DiscGroup()
        self._static_extras: list[StatValue] = []
        self._dynamic_extras: list[StatValue] = []

    @property
    def name(self):
        return self._name

    @property
    def cn_name(self):
        return self._cn_name

    @property
    def level(self):
        return self._level

    @property
    def is_ascension(self):
        return self._is_ascension

    @property
    def repetition(self):
        return self._repetition

    @property
    def skill_levels(self):
        return self._skill_levels

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
    def weapon(self):
        return self._weapon

    @property
    def discs(self):
        return self._discs

    @property
    def static(self):
        return self._static

    @property
    def dynamic(self):
        return self._dynamic

    @property
    def initial(self):
        return self._initial

    # @property
    # def final(self):
    #     return self._final

    def _re_calc(self):
        self._static = self._basic.calc_final()

        # weapon
        self._static.apply_stat(self._weapon.advanced_stat)
        # discs
        for s in self._discs.suit2_stats:
            self._static.apply_stat(s)
        for d in self._discs.discs:
            self._static.apply_stat(d.primary)
            for s in d.secondaries:
                self._static.apply_stat(s)
        # extra
        for s in self._static_extras:
            self._static.apply_stat(s)

        # merge static stats to dynamic
        self._dynamic = self._static.calc_final(self._weapon.atk_base)
        for s in self._dynamic_extras:
            self._dynamic.apply_stat(s)

        # calc initial
        self._initial = self._dynamic.base

    def _fill_data(self):
        self._basic = AgentStats()
        self._basic.base = copy.deepcopy(self._growth.zero)
        self._basic.base.hp += math.floor(self._growth.hp_growth * (self.level - 1))
        self._basic.base.defense += math.floor(
            self._growth.defense_growth * (self.level - 1)
        )
        self._basic.base.atk += math.floor(self._growth.atk_growth * (self.level - 1))
        self._basic.base.crit_ratio = 0.05
        self._basic.base.crit_multi = 0.50

        if not self._ascensions:
            raise Exception("expected ascension data")
        if not self._passives:
            raise Exception("expected passives data")

        asc_rank = (self.level - 1) // 10 + int(
            self.level % 10 == 0 and self.is_ascension
        )
        asc_rank = min(asc_rank, 5)
        stats = itertools.chain(
            self._ascensions[asc_rank], self._passives[self.skill_levels.core]
        )
        for stat in stats:
            self._basic.apply_stat(stat)

        self._re_calc()

    def set_stats(
        self,
        level: int | None = None,
        is_ascension: bool | None = None,
        repetition: int | None = None,
        skill_levels: SkillLevels | None = None,
    ):
        if level is not None:
            self._level = level
        if is_ascension is not None:
            self._is_ascension = is_ascension
        if repetition is not None:
            self._repetition = repetition
        if skill_levels is not None:
            self._skill_levels = skill_levels
        self._fill_data()
        return self

    def set_equipment(
        self,
        weapon: Weapon | None = None,
        discs: DiscGroup | None = None,
        static: list[StatValue] | None = None,
        dynamic: list[StatValue] | None = None,
    ):
        if weapon:
            self._weapon = weapon
        if discs:
            discs.generate_suits()
            self._discs = discs
        if static:
            self._static_extras = static
        if dynamic:
            self._dynamic_extras = dynamic

        self._re_calc()

    def apply_dynamic(self, stats: list[StatValue]):
        for stat in stats:
            self._dynamic.apply_stat(stat)

    def calc_final(self):
        self._final = self._dynamic.calc_final().base

    @abc.abstractmethod
    def gen_hit(self, mark: str) -> GenerateHit:
        pass

    def list_marks(self) -> Sequence[str]:
        return []

    def buffs(self) -> Sequence[Buff]:
        return []

    def all_buffs(self) -> Sequence[Buff]:
        res = list(self.buffs())
        res.extend(self.weapon.buffs())
        if buff := get_suit4_buff(self.discs.suit4):
            res.append(buff)
        return res

    def extra_multiplier(self) -> Sequence[ExtraMultiplier]:
        return []

    def __str__(self):
        self._re_calc()
        return (
            f"{self._name} - {self._attribute.capitalize()}/{self.profession.capitalize()} - {self.camp}"
            + f" - ATK[{self._static.base.atk + self._weapon.atk_base} = {self._static.base.atk} + {self._weapon.atk_base}]\n"
            + f"{self._static.base}\n"
            + f"{self._initial}\n{self._weapon}{self._discs}\n"
        )
