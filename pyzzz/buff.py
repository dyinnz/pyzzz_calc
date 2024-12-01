import abc
from typing import Callable

from pyzzz.model import HitContext, StatValue, StatKind


class Buff:
    def __init__(
        self,
        /,
        kind: StatKind = StatKind.EMPTY,
        owner: str = "",
        source: str = "",
        cov: float = 1.0,
        condition: HitContext | list[HitContext] | None = None,
        for_team: bool = False,
        priority: int = 0,
    ):
        self._kind = kind
        self._owner = owner
        self._source = source
        self._cov = cov
        self.modified_cov = None
        self.enable = 1
        self._condition: list[HitContext] = []
        self._for_team = for_team
        self._priority = priority
        if isinstance(condition, list):
            self._condition.extend(condition)
        elif isinstance(condition, HitContext):
            self._condition.append(condition)

    @property
    def cov(self):
        return self.modified_cov if self.modified_cov is not None else self._cov

    @property
    def key(self):
        return f"{self._owner} {self._kind.with_pct()} {self._source}".strip(" ")

    @property
    def for_team(self):
        return self._for_team

    @property
    def priority(self):
        return self._priority

    @abc.abstractmethod
    def gen_stat(self) -> StatValue:
        pass

    @abc.abstractmethod
    def origin_stat(self) -> StatValue:
        pass

    def active(self, context: HitContext) -> bool:
        if self._condition:
            for cond in self._condition:
                if context.contains(cond):
                    return True
            return False
        return True

    def produce(self, context: HitContext) -> StatValue:
        if self.active(context):
            return self.gen_stat()
        return StatValue.create_empty()

    def __str__(self):
        s = ""
        s += "{:<16}".format(str(self.gen_stat()))
        s += f" from '{self.key}'"
        if self.cov != 1:
            s += f"\tcov={self.cov}"
        return s


class StaticBuff(Buff):
    def __init__(
        self,
        stat: StatValue,
        /,
        owner: str = "",
        source: str = "",
        cov: float = 1.0,
        condition: HitContext | list[HitContext] | None = None,
        for_team: bool = False,
    ):
        super().__init__(
            kind=stat.kind,
            owner=owner,
            source=source,
            cov=cov,
            condition=condition,
            for_team=for_team,
            priority=0,  # always zero
        )
        self.stat = stat

    def origin_stat(self) -> StatValue:
        return StatValue(self.stat.value * self._cov, self.stat.kind)

    def gen_stat(self) -> StatValue:
        return StatValue(self.stat.value * self.cov, self.stat.kind)


class DynamicBuff(Buff):
    def __init__(
        self,
        stat_call: Callable[[], StatValue],
        /,
        owner: str = "",
        source: str = "",
        cov: float = 1.0,
        condition: HitContext | list[HitContext] | None = None,
        for_team: bool = False,
        priority: int = 0,
    ):
        dummy = stat_call()
        super().__init__(
            kind=dummy.kind,
            owner=owner,
            source=source,
            cov=cov,
            condition=condition,
            for_team=for_team,
            priority=priority,
        )
        self.stat_call = stat_call

    def origin_stat(self) -> StatValue:
        stat = self.stat_call()
        return StatValue(stat.value * self._cov, stat.kind)

    def gen_stat(self) -> StatValue:
        stat = self.stat_call()
        return StatValue(stat.value * self.cov, stat.kind)
