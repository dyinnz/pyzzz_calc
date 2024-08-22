from pyzzz.env import Env
from pyzzz.model import *
from pyzzz.delta_analyzer import DeltaAnalyzer

from tests import build_test


def test_ellen():
    from pyzzz.agents.ellen import Ellen

    combo = [Ellen.EX1, Ellen.A3]
    env = Env.from_full(build_test.full_ellen())
    print(env)

    delta = DeltaAnalyzer(env, combo)
    result = delta.quick()
    normal_base = result[0].calc_normal()
    anomaly_base = result[0].calc_anomaly()
    for r in result:
        print(r.show_normal(normal_base))
        # print(r.show_anomaly(anomaly_base))

    # result = env.calc_combo(combo)
    # s = result.show_normal()
    # print(s)


def test_jane():
    from pyzzz.agents.jane import Jane

    # combo = [Jane.A1, Jane.A2, Jane.A3, Jane.A4, Jane.A5, Jane.A6]
    combo = [Jane.Dodge1, Jane.Dodge2, Jane.Dodge3]
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
    test_jane()
