from pyzzz import util
from pyzzz.model import Attribute


class Enemy:
    def __init__(self, level: int = 60, defense_base: int = 60, daze: bool = False):
        self._level = level
        self._defense_base = defense_base
        self._daze = daze
        self._resistances: dict[Attribute, float] = {
            Attribute.All: 0.0,
            Attribute.Physical: 0.0,
            Attribute.Fire: 0.0,
            Attribute.Ice: 0.0,
            Attribute.Electric: 0.0,
            Attribute.Ether: 0.0,
        }

    @property
    def level(self):
        return self._level

    @property
    def defense_base(self):
        return self._defense_base

    @property
    def defense(self) -> float:
        return util.calc_defense(self._level, self._defense_base)

    @property
    def daze(self) -> bool:
        return self._daze

    def resistance(self, attr: Attribute) -> float:
        res = self._resistances[Attribute.All]
        if attr != Attribute.All:
            res += self._resistances[attr]
        return res

    def set_resitance(self, attr: Attribute, value: float):
        self._resistances[attr] += value

    def __str__(self):
        res = ""
        for attr, r in self._resistances.items():
            if r > 0:
                res += f"{attr}+{r * 100:.0f}% "
            elif r < 0:
                res += f"{attr}{r * 100:.0f}% "
        if not res:
            res = "- "
        return f"Enemy{{ L{self._level}, DEF-{self.defense}, {res}}}"


if __name__ == "__main__":
    enemy = Enemy()
    print(enemy)
    enemy.set_resitance(Attribute.Ice, -0.2)
    print(enemy)
