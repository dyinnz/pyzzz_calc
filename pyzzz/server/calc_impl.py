from pyzzz.env import Env
from pyzzz import model
from pyzzz.delta_analyzer import DeltaAnalyzer

import traceback


def calc(input: model.CalcInput):
    print(input)

    env = Env.from_input(input)
    hits = env.agent(0).hits()
    print(env)
    is_anomaly = env.agent(0).profession == model.Profession.Anomaly

    combo_dmg = env.calc_combo(hits)
    hit_dmgs = []
    if is_anomaly:
        hit_dmgs.append(
            {
                "name": "Anomaly",
                "dmg": round(combo_dmg.calc_anomaly(), 1),
                "anomaly_acc": 0.0,
                "detail": combo_dmg.show_anomaly(),
            }
        )

    for dmg in combo_dmg.dmgs:
        hit_dmgs.append(
            {
                "name": dmg.name,
                "dmg": round(dmg.calc_normal(), 1),
                "anomaly_acc": dmg.anomaly_acc,
                "detail": dmg.show_normal(),
            }
        )

    delta_dmgs = []
    try:
        combo = []
        class_dict = env.agent(0).__class__.__dict__
        for hit in input.combo:
            combo.append(class_dict[hit])

        if not combo:
            combo.append(hits[0])

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
                    "ratio": f"{round(delta_value / base_value - 1, 4) * 100}%",
                    "detail": dmg.show_anomaly() if is_anomaly else dmg.show_normal(),
                }
            )
    except Exception as e:
        traceback.print_tb(e.__traceback__)

    return {
        "hit_dmgs": hit_dmgs,
        "delta_dmgs": delta_dmgs,
    }
