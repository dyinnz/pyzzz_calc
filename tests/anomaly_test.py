from pyzzz.dmg import *
from pyzzz.model import *
from tests import build_test


def test_combo():
    from pyzzz.agents.ellen import Ellen

    b = build_test.full_ellen()
    # b.team = []
    b.collect_buffs()

    print(b)
    combo = Combo(AttackList([Ellen.EX1, Ellen.EX2]), b)
    res = combo.delta_analyze()
    print_combo_results(res, True)


def test_grace():
    from pyzzz.agents.grace import Grace

    attacks = AttackList([Grace.EX])
    b = build_test.full_grace()
    b.enemy_base = 54
    b.collect_buffs()
    combo = Combo(attacks, b)
    res = combo.delta_analyze()
    print_combo_results(res, True)


def test_jane():
    from pyzzz.agents.jane import Jane

    attacks = AttackList([Jane.A1, Jane.A2, Jane.A3, Jane.A4, Jane.A5, Jane.A6])
    b = build_test.full_jane()
    b.enemy_base = 60
    b.collect_buffs()
    combo = Combo(attacks, b)
    res = combo.delta_analyze()
    print_combo_results(res, True)


# test_combo()
# test_grace()
test_jane()
