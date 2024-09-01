import typing as t
from pyzzz.model import *
from pyzzz.buff import Buff


class M:
    A1 = "A1"
    A1H = "A1H"
    A2 = "A2"
    A2H = "A2H"
    A3 = "A3"
    A3H = "A3H"
    A3J = "A3J"
    A3K = "A3K"
    A4 = "A4"
    A4H = "A4H"
    A5 = "A5"
    A5H = "A5H"
    A5J = "A5J"
    A6 = "A6"
    A7 = "A7"
    AX1 = "AX1"
    AX1H = "AX1H"
    AX2 = "AX2"
    AX2H = "AX2H"
    AX3 = "AX3"
    AX3H = "AX3H"
    AX4 = "AX4"
    AY1 = "AY1"
    AY2 = "AY2"
    Assit1 = "Assit1"
    Assit2 = "Assit2"
    Chain1 = "Chain1"
    Chain2 = "Chain2"
    Chain3 = "Chain3"
    DAssit1 = "DAssit1"
    DAssit2 = "DAssit2"
    DAssit3 = "DAssit3"
    Dash1 = "Dash1"
    Dash2 = "Dash2"
    Dash3 = "Dash3"
    Dash4 = "Dash4"
    Dash5 = "Dash5"
    Dodge1 = "Dodge1"
    Dodge2 = "Dodge2"
    Dodge3 = "Dodge3"
    E1 = "E1"
    E2 = "E2"
    E3 = "E3"
    E4 = "E4"
    E5 = "E5"
    EX1 = "EX1"
    EX2 = "EX2"
    EX3 = "EX3"
    EX4 = "EX4"
    Final1 = "Final1"
    Final2 = "Final2"
    QAssit1 = "QAssit1"
    QAssit2 = "QAssit2"
    Unknown1 = "Unknown1"
    Unknown2 = "Unknown2"
    Unknown3 = "Unknown3"
    Unknown4 = "Unknown4"


class Hit:
    def __init__(
        self,
        kind: AttackKind = AttackKind.All,
        attribute: Attribute = Attribute.All,
        multi: float = 1.0,
        anomaly: float = 0.0,
        agent: str = "",
        mark: str = "",
        full: str = "",
        tags: set[str] | None = None,
    ):
        self._agent = agent
        self._mark = mark
        self._full = full
        self._kind = kind
        self._attribute = attribute
        self._multi = multi
        self._anomaly = anomaly
        self._tags = set[str]() if tags is None else tags

    @property
    def agent(self):
        return self._agent

    @property
    def qualified(self):
        return f"{self._agent}.{self._mark}"

    @property
    def full(self):
        return self._full

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

    def buffs(self) -> t.Sequence[Buff]:
        return []

    def __str__(self):
        return (
            f"Hit({self._agent}.{self._mark}, {self._full}, kind={self.kind}, attr={self.attribute},"
            + f" multi={self.multi}, anomaly={self.anomaly}, tags={self.tags})"
        )


Attack = Hit
GenerateHit = t.Callable[[], Hit]
