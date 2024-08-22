from typing import Sequence

from pyzzz.buff import Buff
from pyzzz.model import Profession, StatValue, WeaponGrowth


class Weapon:
    def __init__(
        self,
        name: str = "",
        level: int = 60,
        is_ascension: bool = False,
        repetition: int = 1,
    ):
        # from input
        self._name = name
        self._level = level
        self._is_ascension = is_ascension
        self._repetition = repetition

        # from dataset
        self._profession: Profession = Profession.All
        self._init_atk_base: float = 0.0
        self._init_advanced_stat: StatValue = StatValue.create_empty()
        self._growths: list[WeaponGrowth] = []
        self._ascensions: list[WeaponGrowth] = []

        # final stats
        self._atk_base: float = 0.0
        self._advanced_stat: StatValue = StatValue.create_empty()

        self._user: str = ""

    @property
    def name(self):
        return self._name

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
    def atk_base(self) -> float:
        return self._atk_base

    @property
    def advanced_stat(self) -> StatValue:
        return self._advanced_stat

    @property
    def user(self):
        return self._user

    @user.setter
    def set_user(self, user: str):
        self._user = user

    def _fill_data(self):
        rank = (self._level - 1) // 10 + int(
            self._level % 10 == 0 and self._is_ascension
        )
        asc = self._ascensions[rank]
        self._atk_base = round(
            self._init_atk_base
            * (1 + asc.atk_rate + self._growths[self._level].atk_rate)
        )
        self._advanced_stat.value = self._init_advanced_stat.value * (
            1 + asc.primary_rate
        )
        self._advanced_stat.kind = self._init_advanced_stat.kind

    def set_stats(self, level=None, is_ascension=None, repetition=None):
        if level is not None:
            self._level = level
        if is_ascension is not None:
            self._is_ascension = is_ascension
        if repetition is not None:
            self._repetition = repetition
        self._fill_data()

    def buffs(self) -> Sequence[Buff]:
        return []

    def __str__(self):
        return f"{self.name} - {self._profession}\nATK Base: {self._atk_base} Advanced Stat: {self._advanced_stat}"
