from pyzzz.build import *
from pyzzz.model import *


"""
def summary_ellen():
    s = SummaryData()
    s.agent_name = "Ellen"
    s.agent_level = 50
    s.skill_levels = SkillLevels(4, 9, 9, 9, 9, 9)
    s.weapon_name = "CannonRotor"
    s.weapon_level = 50
    s.crit_ratio = 88.2 / 100
    s.crit_multi = 78.8 / 100
    s.green_atk = 1330
    s.suit2 = [DiscKind.Polar_Metal, DiscKind.Woodpecker_Electro]
    s.suit4 = DiscKind.Polar_Metal
    s.disc4 = StatKind.CRIT_RATIO
    s.disc5 = StatKind.ATK_RATIO
    s.team = {"Soukaku": dict(core_skill_atk="1000"), "Lycaon": {}}

    import json
    from dataclasses import asdict

    print(json.dumps(asdict(s), indent=2))

    return Build.from_summary(s)
"""


def full_ellen():
    f = FullBuild()
    f.agent_name = "Ellen"
    f.agent_level = 60
    f.skill_levels = SkillLevels(6, 12, 11, 11, 11, 11)
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
            #     StatValue(19, StatKind.ATK_FLAT),
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
    return f


def full_soukaku():
    f = FullBuild()
    f.agent_name = "Soukaku"
    f.agent_level = 60
    f.agent_rep = 6
    f.skill_levels = SkillLevels(6, 15, 15, 15, 15, 15)
    f.weapon_name = "BashfulDemon"
    f.weapon_level = 60
    f.discs.set(
        Disc(
            1,
            DiscKind.Woodpecker_Electro,
            StatValue.create_empty(),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            2,
            DiscKind.Woodpecker_Electro,
            StatValue(316, StatKind.ATK_FLAT),
            [
                StatValue(0.048, StatKind.CRIT_RATIO),
                StatValue(0.06, StatKind.ATK_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            3,
            DiscKind.Woodpecker_Electro,
            StatValue.create_empty(),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
                StatValue(57, StatKind.ATK_FLAT),
            ],
        )
    )
    f.discs.set(
        Disc(
            4,
            DiscKind.Woodpecker_Electro,
            StatValue(0.24, StatKind.CRIT_RATIO),
            [
                StatValue(0.192, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            5,
            DiscKind.Polar_Metal,
            StatValue(0.24, StatKind.PEN_RATIO),
            [
                StatValue(0.06, StatKind.ATK_RATIO),
                StatValue(0.144, StatKind.CRIT_MULTI),
            ],
            # StatValue(0.30, StatKind.DMG_RATIO),
            # [
            #     StatValue(27, StatKind.PEN_FLAT),
            #     StatValue(0.024, StatKind.CRIT_RATIO),
            # ],
        )
    )
    f.discs.set(
        Disc(
            6,
            DiscKind.Polar_Metal,
            StatValue(0.30, StatKind.ATK_RATIO),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.024, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.team = {"Lycaon": {}}
    return f


def full_soukaku3():
    f = FullBuild()
    f.agent_name = "Soukaku"
    f.agent_level = 60
    f.agent_rep = 6
    f.skill_levels = SkillLevels(4, 15, 15, 15, 15, 15)
    f.weapon_name = "BashfulDemon"
    f.weapon_level = 60
    f.discs.set(
        Disc(
            1,
            DiscKind.Woodpecker_Electro,
            StatValue.create_empty(),
            [
                StatValue(0.072, StatKind.CRIT_RATIO),
                StatValue(0.03, StatKind.ATK_RATIO),
                StatValue(38, StatKind.ATK_FLAT),
            ],
        )
    )
    f.discs.set(
        Disc(
            2,
            DiscKind.Swing_Jazz,
            StatValue(316, StatKind.ATK_FLAT),
            [
                StatValue(0.096, StatKind.CRIT_RATIO),
                StatValue(0.03, StatKind.ATK_RATIO),
                StatValue(0.048, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            3,
            DiscKind.Swing_Jazz,
            StatValue.create_empty(),
            [
                StatValue(0.09, StatKind.ATK_RATIO),
                StatValue(38, StatKind.ATK_FLAT),
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.024, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            4,
            DiscKind.Woodpecker_Electro,
            StatValue(0.48, StatKind.CRIT_MULTI),
            [
                StatValue(0.072, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            5,
            DiscKind.Swing_Jazz,
            StatValue(0.24, StatKind.PEN_RATIO),
            [
                StatValue(0.06, StatKind.ATK_RATIO),
                StatValue(0.144, StatKind.CRIT_MULTI),
            ],
        )
    )
    f.discs.set(
        Disc(
            6,
            DiscKind.Swing_Jazz,
            StatValue(0.30, StatKind.ATK_RATIO),
            [
                StatValue(0.048, StatKind.CRIT_RATIO),
                StatValue(18, StatKind.PEN_FLAT),
            ],
        )
    )
    f.team = {"Lycaon": {}}
    return f


def full_lycaon():
    f = FullBuild()
    f.agent_name = "Lycaon"
    f.agent_level = 60
    f.agent_rep = 0
    f.skill_levels = SkillLevels(6, 11, 11, 11, 11, 11)
    f.weapon_name = "PreciousFossilizedCore"
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
            # DiscKind.Woodpecker_Electro,
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
            # DiscKind.Woodpecker_Electro,
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
            DiscKind.Shockstar_Disco,
            StatValue(0.30, StatKind.DMG_RATIO),
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
            DiscKind.Shockstar_Disco,
            StatValue(0.0, StatKind.IMPACT_RATIO),
            [
                StatValue(0.096, StatKind.CRIT_MULTI),
                StatValue(0.048, StatKind.CRIT_RATIO),
            ],
        )
    )
    f.team = {"Soukaku": dict(core_skill_atk="0")}
    return f


def full_grace():
    f = FullBuild()
    f.agent_name = "Grace"
    f.agent_level = 30
    f.agent_asc = True
    f.agent_rep = 0
    f.skill_levels = SkillLevels(0, 1, 1, 1, 1, 1)
    f.weapon_name = ""
    return f


def full_jane():
    f = FullBuild()
    f.agent_name = "Jane"
    f.agent_level = 60
    f.skill_levels = SkillLevels(6, 11, 11, 11, 11, 11)
    # f.weapon_name = "RainforestGourmet"
    # f.weapon_level = 60
    # f.weapon_rep = 5
    f.weapon_name = "Electro-LipGloss"
    f.weapon_level = 60
    f.weapon_rep = 1
    # f.weapon_name = "FusionCompiler"
    # f.weapon_level = 60
    # f.weapon_rep = 1
    # f.weapon_name = "SharpenedStinger"
    # f.weapon_level = 60
    # f.weapon_rep = 1

    f.discs.set(
        Disc(
            1,
            DiscKind.Freedom_Blues,
            StatValue(0, StatKind.HP_FLAT),
            [
                StatValue(90, StatKind.ANOMALY_PROFICIENCY),
                StatValue(0.3, StatKind.ATK_RATIO),
            ],
        )
    )
    f.discs.set(
        Disc(
            2,
            DiscKind.Freedom_Blues,
            StatValue(316, StatKind.ATK_FLAT),
        )
    )
    f.discs.set(Disc(3, DiscKind.Fanged_Metal, StatValue(0, StatKind.DEF_FLAT), []))
    f.discs.set(
        Disc(
            4,
            DiscKind.Fanged_Metal,
            StatValue(90, StatKind.ANOMALY_PROFICIENCY),
        )
    )
    f.discs.set(
        Disc(
            5,
            DiscKind.Fanged_Metal,
            StatValue(0.3, StatKind.DMG_RATIO),
        )
    )
    f.discs.set(
        Disc(
            6,
            DiscKind.Fanged_Metal,
            StatValue(0.3, StatKind.ANOMALY_MASTER),
        )
    )
    return f


if __name__ == "__main__":
    # res = full_ellen()
    # res = full_grace()
    res = full_jane()
    print(res)
