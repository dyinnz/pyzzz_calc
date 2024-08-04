from typing import Optional

from pyzzz.model import AttackKind, ContextData, StatKind, StatValue


class Buff:

    def __init__(self, stat: StatValue, **kw):
        self.stat = stat
        self.source = kw.get("source", "")
        self.cov = kw.get("cov", 1.0)
        self.duration = kw.get("duration", 0.0)  # zero for static buf
        self.condition: Optional[ContextData] = kw.get("condition", None)

    def produce(self, context: ContextData) -> StatValue:
        if self.active(context):
            return StatValue(self.stat.value * self.cov, self.stat.kind)
        return StatValue.empty()

    def active(self, c: ContextData) -> bool:
        if self.condition:
            if c.contains(self.condition):
                return True
            return False
        return True

    def coverage(self) -> float:
        return self.cov

    def __str__(self):
        if self.cov < 1.0:
            return f"{self.stat} * {self.cov} from '{self.source}'"
        else:
            return f"{self.stat} from '{self.source}'"
