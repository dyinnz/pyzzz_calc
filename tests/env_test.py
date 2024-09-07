from pyzzz.env import Env
from pyzzz.model import *
from pyzzz.delta_analyzer import DeltaAnalyzer
from pyzzz.hit import M
from pyzzz.dataset.marks import Lucy
from pyzzz.agents import create_agent, from_agent_build

from tests import build_test


def test_ellen():
    combo = [
        M.EX1,
        M.AX3,
    ]
    env = Env.from_full(build_test.full_ellen())
    # env.disable('Swing_Jazz suit4 DMG +15%')

    env2 = Env.from_full(build_test.full_soukaku())
    env.set_agent(1, env2.agent(0))

    print(env)

    result = env.calc_combo(combo)
    s = result.show_normal()
    print(s)

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
    env.disable_buf("Soukaku core skill atk dynamic flat")
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
    combo = [M.A1, M.A2, M.A3, M.A4, M.A5, M.A6, M.E1, M.EX1]
    # combo = [M.A6]
    env = Env.from_full(build_test.full_jane())
    env.set_agent(1, create_agent(name="Seth"))
    env.set_agent(2, create_agent(name="Lucy", core_skill_atk=600))
    print(env)

    result = env.calc_combo(combo)
    print(result.show_normal())
    print(result.show_anomaly())

    # delta = DeltaAnalyzer(env, combo)
    # result = delta.quick()
    # normal_base = result[0].calc_normal()
    # anomaly_base = result[0].calc_anomaly()
    # for r in result:
    #     print(r.show_normal(normal_base))
    #     print(r.show_anomaly(anomaly_base))


def test_lucy():
    env = Env()
    env.set_agent(0, from_agent_build(build_test.full_lucy()))
    print(env)
    # combo = env.agent(0).list_marks()
    # combo = [Lucy.Chain1, Lucy.EX2, Lucy.EX2, Lucy.EX2]
    combo = [Lucy.NIL1, Lucy.NIL2, Lucy.NIL3, Lucy.NIL4]
    result = env.calc_combo(combo)
    print(result.show_normal())

    delta = DeltaAnalyzer(env, combo)
    result = delta.quick()
    normal_base = result[0].calc_normal()
    for r in result:
        print(r.show_normal(normal_base))


if __name__ == "__main__":
    test_ellen()
    # test_lycaon()
    # test_jane()
    # test_soukaku()
    # test_lucy()
