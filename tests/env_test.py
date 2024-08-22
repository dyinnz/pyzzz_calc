from pyzzz.build import FullBuild
from pyzzz.model import *
from pyzzz.env import Env, DeltaAnalyzer


def full_ellen():
    f = FullBuild()
    f.agent_name = "Ellen"
    f.agent_level = 60
    f.skill_levels = SkillLevels(6, 10, 10, 10, 10, 10)
    f.weapon_name = "CannonRotor"
    f.weapon_level = 60
    f.discs.set(
        Disc(
            1,
            DiscKind.Woodpecker_Electro,
            StatValue.create_empty(),
            [
                StatValue(0.144, StatKind.CRIT_MULTI),
                StatValue(0.072, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            2,
            DiscKind.Woodpecker_Electro,
            StatValue(316, StatKind.ATK_FLAT),
            [
                StatValue(0.072, StatKind.CRIT_RATIO),
                StatValue(0.06, StatKind.ATK_RATIO),
                StatValue(0.048, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            3,
            DiscKind.Polar_Metal,
            StatValue.create_empty(),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.072, StatKind.CRIT_RATIO),
                StatValue(18, StatKind.ANOMALY_PROFICIENCY),
            ],
        )
    )
    f.discs.set(
        Disc(
            4,
            DiscKind.Polar_Metal,
            StatValue(0.48, StatKind.CRIT_MULTI),
            [
                StatValue(0.03, StatKind.ATK_RATIO),
                StatValue(18, StatKind.PEN_FLAT),
                StatValue(0.048, StatKind.CRIT_RATIO),
                StatValue(57, StatKind.ATK_FLAT),
            ],
            # [
            #     StatValue(0.12, StatKind.ATK_RATIO),
            #     StatValue(19, StatKind.PEN_FLAT),
            #     StatValue(0.024, StatKind.CRIT_RATIO),
            # ],
        )
    )
    f.discs.set(
        Disc(
            5,
            DiscKind.Polar_Metal,
            StatValue(0.30, StatKind.ATK_RATIO),
            [
                StatValue(19, StatKind.ATK_FLAT),
                StatValue(0.048, StatKind.CRIT_RATIO),
                StatValue(18, StatKind.PEN_FLAT),
                StatValue(0.144, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            6,
            DiscKind.Polar_Metal,
            StatValue(0.30, StatKind.ATK_RATIO),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.team = {"Soukaku": dict(core_skill_atk="1000"), "Lycaon": {}}
    return Env.from_full(f)


def test_env():
    from pyzzz.agents.ellen import Ellen

    combo = [Ellen.EX1, Ellen.A3]

    env = full_ellen()
    print(env)

    delta = DeltaAnalyzer(env, combo)
    result = delta.quick()
    normal_base = result[0].calc_normal()
    anomaly_base = result[0].calc_anomaly()
    for r in result:
        print(r.show_normal(normal_base))
        print(r.show_anomaly(anomaly_base))

    # result = env.calc_combo(combo)
    # s = result.show_normal()
    # print(s)


if __name__ == "__main__":
    test_env()
