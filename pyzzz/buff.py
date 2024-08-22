import abc
from typing import Callable

from pyzzz.model import HitContext, StatValue


class Buff:
    def __init__(
        self,
        source: str = "",
        cov: float = 1.0,
        condition: HitContext | list[HitContext] | None = None,
        for_team: bool = False,
    ):
        self.source = source
        self.cov = cov
        self.condition: list[HitContext] = []
        self.for_team = for_team
        if isinstance(condition, list):
            self.condition.extend(condition)
        elif isinstance(condition, HitContext):
            self.condition.append(condition)

    @abc.abstractmethod
    def gen_stat(self) -> StatValue:
        pass

    def active(self, context: HitContext) -> bool:
        if self.condition:
            for cond in self.condition:
                if context.contains(cond):
                    return True
            return False
        return True

    def produce(self, context: HitContext) -> StatValue:
        if self.active(context):
            return self.gen_stat()
        return StatValue.create_empty()

    def __str__(self):
        if self.cov < 1.0:
            return f"{self.gen_stat()} with cov={self.cov} from '{self.source}'"
        else:
            return f"{self.gen_stat()} from '{self.source}'"


class StaticBuff(Buff):
    def __init__(
        self,
        stat: StatValue,
        source: str = "",
        cov: float = 1.0,
        condition: HitContext | list[HitContext] | None = None,
        for_team: bool = False,
    ):
        super().__init__(source, cov, condition, for_team)
        self.stat = stat

    def gen_stat(self) -> StatValue:
        return StatValue(self.stat.value * self.cov, self.stat.kind)


class DynamicBuff(Buff):
    def __init__(
        self,
        stat_call: Callable[[], StatValue],
        source: str = "",
        cov: float = 1.0,
        condition: HitContext | list[HitContext] | None = None,
        for_team: bool = False,
    ):
        super().__init__(source, cov, condition, for_team)
        self.stat_call = stat_call

    def gen_stat(self) -> StatValue:
        stat = self.stat_call()
        return StatValue(stat.value * self.cov, stat.kind)
