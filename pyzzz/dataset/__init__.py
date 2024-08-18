import copy
import csv
import os
from functools import lru_cache

from pyzzz.model import AgentData, StatKind, StatValue, WeaponGrowth

file_path = os.path.realpath(__file__)
directory = os.path.dirname(file_path)


def get_percent(s):
    return float(s[:-1]) / 100


@lru_cache
def load_agents_basic():
    agents = {}

    with open(directory + "/agents_basic.csv", encoding="utf-8") as file:
        spamreader = csv.reader(file, delimiter="\t")
        for row in spamreader:
            name = row[0]

            agent = AgentData()
            # agent.name = row[0]
            agent.level = 60
            # agent.hp = float(row[1])
            # agent.atk = float(row[2])
            # agent.defense = float(row[3])
            agent.crit_ratio = get_percent(row[4])
            agent.crit_multi = get_percent(row[5])
            agent.impact = float(row[6])
            agent.anomaly_master = float(row[7])
            # anergy limit
            agent.energy_regen = float(row[9])
            agent.anomaly_proficiency = float(row[10])
            agent.hp = float(row[11])
            agent.atk = float(row[12])
            agent.defense = float(row[13])

            agents[name] = agent

    return agents


@lru_cache
def load_skills():
    skills = {}

    with open(directory + "/skills.csv", encoding="utf-8") as file:
        spamreader = csv.reader(file, delimiter="\t")
        header = True
        for row in spamreader:
            if header:
                header = False
                continue
            if not row:
                continue
            agent = row[0]
            skill_name = row[1] + "-" + row[2]

            agent_skill = skills.get(agent, {})
            item = {}
            item["dmg"] = get_percent(row[3])
            item["dmg_grow"] = get_percent(row[4])
            item["impact"] = get_percent(row[5])
            item["impact_grow"] = get_percent(row[6])
            item["energy"] = get_percent(row[7])
            item["noise"] = float(row[8])
            item["anomaly"] = float(row[9])
            if len(row) > 10:
                item["distance"] = row[10]
            else:
                item["distance"] = ""
            agent_skill[skill_name] = item
            skills[agent] = agent_skill

    return skills


@lru_cache
def load_zzz_gg_agents_json():
    import json

    with open(directory + "/zzz.gg.agents.json", encoding="utf-8") as file:
        return json.load(file)


@lru_cache
def load_zzz_gg_agents():
    def remove_skills_talents(agent):
        # agent.pop("Skills")
        # agent.pop("Talents")
        return agent

    json = load_zzz_gg_agents_json()

    properties_list = json["properties"]
    properties_by_id = {prop["PropID"]: prop for prop in properties_list}
    # fix strange id
    properties_by_id[20101] = properties_by_id[201]
    properties_by_id[21101] = properties_by_id[211]
    properties_by_id[23101] = properties_by_id[231]

    elements_by_id = {
        item["DamageElementID"]: item["Name"] for item in json["elements"]
    }
    professions_by_id = {item["ID"]: item["Name"] for item in json["professions"]}

    agents_list = json["characters"]
    for agent in agents_list:
        remove_skills_talents(agent)
    # 0
    id2name = {agent["ID"]: agent["Name"] for agent in agents_list}

    # 1
    agents_dict = {agent["Name"]: agent for agent in agents_list}
    for v in agents_dict.values():
        v["ElementTypeName"] = elements_by_id[v["ElementTypes"][0]]
        v["ProfessionName"] = professions_by_id[v["WeaponType"]]

    # 2
    ascensions_dict = {}
    ascensions_list = json["ascension"]
    for ascension in ascensions_list:
        id = ascension["AvatarID"]
        if id not in id2name:
            continue

        name = id2name[id]
        rank = ascension["Rank"]
        agent_asc = ascensions_dict.get(name, {})
        agent_asc[rank] = ascension
        ascensions_dict[name] = agent_asc

    passives_dict = {}
    passives_list = json["passives"]
    for passive in passives_list:
        id = passive["AvatarID"]
        if id not in id2name:
            continue

        extra = passive["Extra"]
        props = {
            properties_by_id[prop["Property"]]["Name"]: prop["Value"] for prop in extra
        }

        name = id2name[id]
        max_level = passive["MaxLevel"]
        agent_passive = passives_dict.get(name, {})
        agent_passive[max_level] = props
        passives_dict[name] = agent_passive

    return dict(agents=agents_dict, ascensions=ascensions_dict, passives=passives_dict)


@lru_cache
def load_zzz_gg_weapons_json():
    import json

    with open(directory + "/zzz.gg.weapons.json", encoding="utf-8") as file:
        return json.load(file)


@lru_cache
def load_zzz_gg_weapons():

    json = load_zzz_gg_weapons_json()

    professions_by_id = {item["ID"]: item["Name"] for item in json["professions"]}

    model_ascension: dict[int, list[WeaponGrowth]] = {}
    model_leveling: dict[int, list[WeaponGrowth]] = {}
    weapons = {}

    ascensions = json["ascension"]
    for item in ascensions:
        model = item["Rarity"]
        model_asc = model_ascension.get(model, [])

        growth = WeaponGrowth()
        growth.atk_rate = item["StarRate"] / 1e4
        growth.primary_rate = item["RandRate"] / 1e4
        model_asc.append(growth)

        model_ascension[model] = model_asc

    levelings = json["leveling"]
    for item in levelings:
        model = item["Rarity"]
        model_lv = model_leveling.get(model, [])

        growth = WeaponGrowth()
        growth.atk_rate = item["EnhanceRate"] / 1e4
        model_lv.append(growth)

        model_leveling[model] = model_lv

    engines = json["engines"]
    weapons = {item["Name"].replace(" ", ""): item for item in engines}
    for v in weapons.values():
        v["ProfessionName"] = professions_by_id[v["Type"]]

    return dict(weapons=weapons, levelings=model_leveling, ascensions=model_ascension)


ZZZ_GG_STAT_PASSIVE = {
    "ATK": StatKind.ATK_FLAT,
    "Impact": StatKind.IMPACT,
    "CRIT Rate": StatKind.CRIT_RATIO,
    "CRIT DMG": StatKind.CRIT_MULTI,
    "Energy Regen": StatKind.ENERGY_REGEN,
    "Anomaly Mastery": StatKind.ANOMALY_MASTER,
    "Anomaly Proficiency": StatKind.ANOMALY_PROFICIENCY,
    "PEN Ratio": StatKind.PEN_RATIO,
}


ZZZ_GG_STAT_PRIMARY = copy.deepcopy(ZZZ_GG_STAT_PASSIVE)
ZZZ_GG_STAT_PRIMARY["ATK"] = StatKind.ATK_RATIO
ZZZ_GG_STAT_PRIMARY["DEF"] = StatKind.DEF_RATIO
ZZZ_GG_STAT_PRIMARY["HP"] = StatKind.HP_RATIO
