import abc
from typing import Callable

from pyzzz.model import ContextData, StatValue


class BuffBase:
    def __init__(
        self,
        source: str = "",
        cov: float = 1.0,
        condition: ContextData | list[ContextData] | None = None,
        for_team: bool = True,
    ):
        self.source = source
        self.cov = cov
        self.condition: list[ContextData] = []
        self.for_team = for_team
        if isinstance(condition, list):
            self.condition.extend(condition)
        elif isinstance(condition, ContextData):
            self.condition.append(condition)

    @abc.abstractmethod
    def produce(self, context: ContextData | None) -> StatValue:
        pass

    def active(self, context: ContextData | None) -> bool:
        if context and self.condition:
            for cond in self.condition:
                if context.contains(cond):
                    return True
            return False
        return True

    def __str__(self):
        if self.cov < 1.0:
            return f"{self.produce(None)} with cov={self.cov} from '{self.source}'"
        else:
            return f"{self.produce(None)} from '{self.source}'"


class Buff(BuffBase):
    def __init__(self, stat: StatValue, **kw):
        BuffBase.__init__(self, **kw)
        self.stat = stat

    def produce(self, context: ContextData | None) -> StatValue:
        if self.active(context):
            return StatValue(self.stat.value * self.cov, self.stat.kind)
        return StatValue.create_empty()


class DynamicBuff(BuffBase):
    def __init__(self, stat_call: Callable[[], StatValue], **kw):
        BuffBase.__init__(self, **kw)
        self.stat_call = stat_call

    def produce(self, context: ContextData | None) -> StatValue:
        if self.active(context):
            stat = self.stat_call()
            return StatValue(stat.value * self.cov, stat.kind)
        return StatValue.create_empty()
