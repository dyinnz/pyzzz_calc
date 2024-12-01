from pyzzz.env import Env
from pyzzz import model
from pyzzz.delta_analyzer import DeltaAnalyzer

import copy
import traceback


def calc_hit_dmgs(env: Env):
    is_anomaly = env.agent(0).profession == model.Profession.Anomaly

    hit_marks = env.agent(0).list_marks()

    combo_dmg = env.calc_combo(hit_marks)
    hit_dmgs = []
    if is_anomaly:
        hit_dmgs.append(
            {
                "name": "异常伤害",
                "mark": "Anomaly",
                "dmg": round(combo_dmg.calc_anomaly(), 1),
                "anomaly_acc": 0.0,
                "detail": combo_dmg.show_anomaly(),
            }
        )

    for dmg in combo_dmg.dmgs:
        hit_dmgs.append(
            {
                "name": dmg.hit._full,
                "mark": dmg.hit.qualified,
                "dmg": round(dmg.calc_normal(), 1),
                "anomaly_acc": dmg.anomaly_acc,
                "detail": dmg.show_normal(),
            }
        )
    return hit_dmgs


def calc_delta_dmgs(env: Env):
    is_anomaly = env.agent(0).profession == model.Profession.Anomaly

    delta_dmgs = []
    try:
        combo = []
        if not combo:
            combo.append("EX1")

        analyzer = DeltaAnalyzer(env, combo)
        analyzer_dmg = analyzer.quick()

        base_value = (
            analyzer_dmg[0].calc_anomaly()
            if is_anomaly
            else analyzer_dmg[0].calc_normal()
        )

        for dmg in analyzer_dmg:
            delta_value = dmg.calc_anomaly() if is_anomaly else dmg.calc_normal()
            delta_dmgs.append(
                {
                    "name": dmg.comment,
                    "ratio": delta_value / base_value - 1,
                    "detail": dmg.show_anomaly() if is_anomaly else dmg.show_normal(),
                }
            )
    except Exception as e:
        traceback.print_tb(e.__traceback__)

    return delta_dmgs


def calc_agent_initials(env: Env):
    initials = []
    initials.append(copy.deepcopy(env.agent(0).initial))
    initials.append(copy.deepcopy(env.agent(1).initial))
    initials.append(copy.deepcopy(env.agent(2).initial))

    for i, stats in enumerate(initials):
        stats.dmg_ratio = stats.calc_dmg_ratio(env.agent(i).attribute)

    return initials


def collect_buffs(env: Env):
    result = []

    total_buffs = env.collect_buffs()
    for idx, agent_buffs in enumerate(total_buffs):
        for key, buff in agent_buffs.items():
            result.append(
                model.BuffModel(
                    idx=idx,
                    key=key,
                    origin_cov=buff._cov,
                    cov=buff._cov,
                    stat_str=str(buff.origin_stat()),
                )
            )

    return result


def calc(input: model.CalcInput):
    print(input)

    env = Env.from_input(input)
    env._modified_buffs = input.buffs
    env.prepare()


    return {
        "hit_dmgs": calc_hit_dmgs(env),
        "delta_dmgs": calc_delta_dmgs(env),
        "initials": calc_agent_initials(env),
        "buffs": collect_buffs(env),
    }
