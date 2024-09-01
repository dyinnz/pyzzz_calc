from pyzzz.env import Env
from pyzzz.model import *
from pyzzz.delta_analyzer import DeltaAnalyzer
from pyzzz.hit import M

from tests import build_test


def test_ellen():
    combo = [
        M.EX1,
        M.A3,
    ]
    env = Env.from_full(build_test.full_ellen())
    # env.disable('Swing_Jazz suit4 DMG +15%')

    env2 = Env.from_full(build_test.full_soukaku())
    env.set_agent(1, env2.agent(0))

    print(env)

    # result = env.calc_combo(combo)
    # s = result.show_normal()
    # print(s)

    delta = DeltaAnalyzer(env, combo)
    result = delta.quick()
    normal_base = result[0].calc_normal()
    for r in result:
        print(r.show_normal(normal_base))


def test_lycaon():
    combo = [M.Chain1]
    env = Env.from_full(build_test.full_lycaon())
    print(env)

    delta = DeltaAnalyzer(env, combo)
    result = delta.quick()
    normal_base = result[0].calc_normal()
    for r in result:
        print(r.show_normal(normal_base))


def test_soukaku():
    combo = [M.Chain1, M.E3]
    env = Env.from_full(build_test.full_soukaku3())
    env.disable("Soukaku core skill atk dynamic flat")
    # env.disable('Soukaku rep4 ice res ratio')

    print(env)
    result = env.calc_combo(combo)
    print(result.show_normal())

    # delta = DeltaAnalyzer(env, combo)
    # result = delta.quick()
    # normal_base = result[0].calc_normal()
    # for r in result:
    #     print(r.show_normal(normal_base))

    combo = [M.Final1, M.Dash2, M.AX3]
    env = Env.from_full(build_test.full_soukaku3())
    result = env.calc_combo(combo)
    print(result.show_normal())


def test_jane():
    combo = [M.A1, M.A2, M.A3, M.A4, M.A5, M.A6]
    env = Env.from_full(build_test.full_jane())
    print(env)

    hits = env.calc_combo(combo)

    print(env.agent(0).__class__.__dict__)

    # delta = DeltaAnalyzer(env, combo)
    # result = delta.quick()
    # normal_base = result[0].calc_normal()
    # anomaly_base = result[0].calc_anomaly()
    # for r in result:
    #     print(r.show_normal(normal_base))
    #     print(r.show_anomaly(anomaly_base))


if __name__ == "__main__":
    test_ellen()
    test_lycaon()
    test_jane()
    test_soukaku()
