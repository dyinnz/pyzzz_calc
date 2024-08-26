from pyzzz.env import Env
from pyzzz.model import *
from pyzzz.delta_analyzer import DeltaAnalyzer

from tests import build_test


def test_ellen():
    from pyzzz.agents.ellen import Ellen

    # combo = [
    #     Ellen.Chain,
    #     Ellen.Final,
    #     Ellen.A1,
    #     Ellen.A2,
    #     Ellen.A3,
    #     Ellen.EX1,
    # ]
    combo = [
        Ellen.EX1,
        Ellen.A3,
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
    from pyzzz.agents.lycaon import Lycaon

    combo = [Lycaon.Chain]
    env = Env.from_full(build_test.full_lycaon())
    print(env)

    delta = DeltaAnalyzer(env, combo)
    result = delta.quick()
    normal_base = result[0].calc_normal()
    for r in result:
        print(r.show_normal(normal_base))


def test_soukaku():
    from pyzzz.agents.soukaku import Soukaku

    combo = [Soukaku.Chain, Soukaku.EY1]
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

    combo = [Soukaku.Final, Soukaku.Dash, Soukaku.A3]
    env = Env.from_full(build_test.full_soukaku3())
    result = env.calc_combo(combo)
    print(result.show_normal())


def test_jane():
    from pyzzz.agents.jane import Jane

    combo = [Jane.A1, Jane.A2, Jane.A3, Jane.A4, Jane.A5, Jane.A6]
    # combo = [Jane.Dodge1, Jane.Dodge2, Jane.Dodge3]
    env = Env.from_full(build_test.full_jane())
    print(env)

    delta = DeltaAnalyzer(env, combo)
    result = delta.quick()
    normal_base = result[0].calc_normal()
    anomaly_base = result[0].calc_anomaly()
    for r in result:
        print(r.show_normal(normal_base))
        print(r.show_anomaly(anomaly_base))


if __name__ == "__main__":
    # test_ellen()
    # test_lycaon()
    test_jane()
    # test_soukaku()
