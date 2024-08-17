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


test_combo()
