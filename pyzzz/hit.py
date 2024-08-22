from typing import Sequence
from pyzzz.model import *
from pyzzz.buff import Buff


class Hit:
    def __init__(
        self,
        kind: AttackKind = AttackKind.All,
        attribute: Attribute = Attribute.All,
        multi: float = 1.0,
        anomaly: float = 0.0,
        agent: str = "",
        tags: set[str] | None = None,
    ):
        self._agent = agent
        self._kind = kind
        self._attribute = attribute
        self._multi = multi
        self._anomaly = anomaly
        self._tags = set[str]() if tags is None else tags

    @property
    def kind(self):
        return self._kind

    @property
    def attribute(self):
        return self._attribute

    @property
    def multi(self):
        return self._multi

    @property
    def anomaly(self):
        return self._anomaly

    @property
    def tags(self):
        return self._tags

    def buffs(self) -> Sequence[Buff]:
        return []


Attack = Hit
