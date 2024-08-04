import copy

from pyzzz import dataset
from pyzzz.buff import Buff
from pyzzz.model import StatKind, StatValue, WeaponData

BUFFS = {
    "CannonRotor": Buff(
        StatValue(0.075, StatKind.ATK_RATIO), source="CannonRotor buff"
    ),
    "StarlightEngine": Buff(
        StatValue(0.192, StatKind.ATK_RATIO), source="StarlightEngine buff"
    ),
}

CN2EN = {
    "加农转子": "CannonRotor",
    "街头巨星": "StarlightEngine",
}

EN2CN = {v: k for k, v in CN2EN.items()}


class Weapon:
    def __init__(self):
        self.name = ""
        self.cn_name = ""
        self.data: WeaponData = WeaponData(0, 0, StatValue.empty())
        self.origin_data = copy.deepcopy(self.data)
        self.buffs: list[Buff] = []


def get_weapon(n: str, cov=1.0) -> Weapon:
    name = n
    cn_name = n
    if n.isascii():
        cn_name = EN2CN[n]
    else:
        name = CN2EN[n]

    db = dataset.load_weapons()[cn_name]

    weapon = Weapon()
    weapon.name = name
    weapon.cn_name = cn_name
    weapon.data.level = 60
    weapon.data.atk = db["atk"]
    weapon.data.primary = db["primary"]

    weapon.origin_data = copy.deepcopy(weapon.data)

    buff = BUFFS.get(weapon.name, None)
    if buff:
        buff.cov = cov
        weapon.buffs.append(buff)

    return weapon
