from functools import reduce
from pyzzz import util

from pyzzz.model import Attribute


class Number:
    def __init__(self, v, source=""):
        if isinstance(v, Number):
            self.v = v.value()
            self.source = v.source
        else:
            self.v = v
            self.source = ""
        if source:
            self.source = source

    def __add__(self, rhs):
        return Number(self.v + rhs.value())

    def __mul__(self, rhs):
        return Number(self.v * rhs.value())

    def __sub__(self, rhs):
        return Number(self.v - rhs.value())

    def __truediv__(self, rhs):
        return Number(self.v / rhs.value())

    def __neg__(self):
        return Number(-self.v)

    def value(self):
        return self.v

    def __str__(self):
        return f"{self.v:.3f}".rstrip("0").rstrip(".")


class LazyAdd:
    def __init__(self, numbers, source=""):
        self.numbers = [Number(n) for n in numbers]
        self.source = source

    def add(self, n: float | Number):
        self.numbers.append(Number(n))

    def set(self, n: float | Number):
        self.numbers = [Number(n)]

    def value(self):
        return reduce(lambda x, y: x + y, self.numbers, Number(0.0)).value()

    def __str__(self):
        if not self.numbers:
            return "0"
        s = "+".join([str(n) for n in self.numbers])
        if len(self.numbers) > 1:
            s = "(" + s + ")"
        return s


class ListMultiplier(LazyAdd):
    def __init__(self, numbers=None):
        if numbers is None:
            numbers = [1.0]
        LazyAdd.__init__(self, numbers)

    def calc(self):
        return self


# 1.1
class ATKMultiplier:
    def __init__(self):
        self.agent = Number(0.0)
        self.weapon = Number(0.0)
        self.static_ratio = LazyAdd([1.0])
        self.static_flat = LazyAdd([])
        self.dynamic_ratio = LazyAdd([1.0])
        self.dynamic_flat = LazyAdd([])

    def calc(self):
        return (
            (self.agent + self.weapon) * self.static_ratio + self.static_flat
        ) * self.dynamic_ratio + self.dynamic_flat

    def __str__(self):
        return f"( ({self.agent + self.weapon} * {self.static_ratio} + {self.static_flat}) * {self.dynamic_ratio} + {self.dynamic_flat} )"


# 1.2
SkillMultiplier = ListMultiplier

# 2
DMGMultiplier = ListMultiplier

# 3
ResistanceMutiplier = ListMultiplier


# 4
class DefenseMultiplier:
    def __init__(self):
        self.agent = Number(util.calc_defense(60))
        self.enemy = Number(util.calc_defense(70))

        self.pen_ratio = LazyAdd([])
        self.pen_flat = LazyAdd([])
        self.enemy_def_ratio = LazyAdd([])

    def set_agent(self, level):
        self.agent = Number(util.calc_defense(level))

    def set_enemy(self, level, base):
        self.enemy = Number(util.calc_defense(level, base))

    def calc(self):
        return self.agent / (
            self.agent
            + self.enemy
            * (Number(1.0) + self.enemy_def_ratio)
            * (Number(1.0) - self.pen_ratio)
            - self.pen_flat
        )

    def __str__(self):
        pen = (Number(1.0) - self.pen_ratio) * (Number(1.0) + self.enemy_def_ratio)
        return f"{self.agent}/({self.agent} + {self.enemy} * {pen} - {self.pen_flat})"


# 5
class CriticalMultiplier:
    def __init__(self):
        self.ratio = LazyAdd([])
        self.multi = LazyAdd([])

    def calc(self):
        ratio = self.ratio.value()
        if ratio > 1.0:
            ratio = 1.0
        return Number(1.0) + Number(ratio * self.multi.value())

    def __str__(self):
        ratio = self.ratio.value()
        if ratio > 1.0:
            return f"(1 + 1 * {self.multi})"
        else:
            return f"(1 + {self.ratio} * {self.multi})"


# 7
DazeMultiplier = ListMultiplier


# ap
class AnomalyProficiencyMultiplier(LazyAdd):
    def __init__(self):
        LazyAdd.__init__(self, [])

    def calc(self):
        return Number(self.value() / 100.0)

    def __str__(self):
        return f"({super().__str__()} /100)"


class AnomalyAttributeMultiplier:
    def __init__(self):
        self.attribute = Attribute.All
        pass

    def calc(self):
        v = 0.0
        if self.attribute == Attribute.Fire:
            v = 0.5 * 20
        elif self.attribute == Attribute.Electric:
            v = 1.25 * 10
        elif self.attribute == Attribute.Ether:
            v = 0.625 * 20
        elif self.attribute == Attribute.Ice:
            v = 5
        elif self.attribute == Attribute.Physical:
            v = 7.13
        return Number(v)

    def __str__(self):
        return f"{self.calc()}"


class AnomalyLevelMultiplier:
    def __init__(self):
        self.level = 60
        pass

    def calc(self):
        return Number(round(1 + 1 / 59 * (self.level - 1), 4))

    def __str__(self):
        return f"{self.calc()}"
