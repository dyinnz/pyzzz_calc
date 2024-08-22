from typing import Sequence
import copy
import itertools
from pyzzz.model import *
from pyzzz.buff import Buff
from pyzzz.weapon import Weapon
from pyzzz.discs import get_suit4_buff


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
        self._growth = AgentDataWithGrowth()
        self._ascensions: list[list[StatValue]] = []
        self._passives: list[list[StatValue]] = []
        self._skill = {}

        # final stats board
        self._basic = AgentData()  # init + growth
        self._weapon = Weapon()
        self._discs = DiscGroup()
        self._extras = list[StatValue]()

        self._static = AgentData()  # data + weapon + discs + extra

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
    def without_weapon(self):
        return self._basic

    @property
    def weapon(self):
        return self._weapon

    @property
    def discs(self):
        return self._discs

    @property
    def static(self):
        return self._static

    def _calc_static(self):
        # basic
        self._static = copy.deepcopy(self._basic)
        # weapon
        self._static.atk_weapon = self._weapon.atk_base
        self._static.apply_stat(self._weapon.advanced_stat)
        # discs
        for s in self._discs.suit2_stats:
            self._static.apply_stat(s)
        for d in self._discs.discs:
            self._static.apply_stat(d.primary)
            for s in d.secondaries:
                self._static.apply_stat(s)
        # extra
        for s in self._extras:
            self._static.apply_stat(s)

    def _fill_data(self):
        self._basic = copy.deepcopy(self._growth.init)
        self._basic.hp_base += round(self._growth.hp_growth * (self.level - 1))
        self._basic.def_base += round(self._growth.defense_growth * (self.level - 1))
        self._basic.atk_base += round(self._growth.atk_growth * (self.level - 1))

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

        self._calc_static()

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
        extras: list[StatValue] | None = None,
    ):
        weapon_atk_changed = weapon and weapon.atk_base != self._weapon.atk_base
        if weapon:
            self._weapon = weapon
        if discs:
            self._discs = discs
        if extras:
            self._extras = extras

        if weapon_atk_changed:
            self._fill_data()
        else:
            self._calc_static()

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

    def debug_str(self):
        return f"{self}\n{self._growth}\n{self._ascensions}\n{self._passives}\n"

    def __str__(self):
        return f"{self._name} - {self._camp}/{self._profession}/{self._attribute}\n{self._static}\n{self._weapon}\n{self._discs}\n"
