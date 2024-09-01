import copy
import csv
import os
from functools import lru_cache

from pyzzz.model import *

file_path = os.path.realpath(__file__)
directory = os.path.dirname(file_path)


def get_percent(s):
    return float(s[:-1]) / 100


def map_cn_index(name):
    if name.startswith("一段"):
        return 1
    if name.startswith("二段"):
        return 2
    if name.startswith("三段"):
        return 3
    if name.startswith("四段"):
        return 4
    if name.startswith("五段"):
        return 5
    if name.startswith("六段"):
        return 6
    if name.startswith("七段"):
        return 7
    if name.startswith("八段"):
        return 8
    if name.startswith("九段"):
        return 9
    return 0


def map_atk_kind(name):
    if name.startswith("普通攻击"):
        return AttackKind.Basic
    elif name.startswith("冲刺攻击"):
        return AttackKind.Dash
    elif name.startswith("闪避反击"):
        return AttackKind.Dodge
    elif name.startswith("快速支援"):
        return AttackKind.QuickAssit
    elif name.startswith("招架支援"):
        return AttackKind.DefenseAssit
    elif name.startswith("支援突击"):
        return AttackKind.Assit
    elif name.startswith("特殊技"):
        return AttackKind.Special
    elif name.startswith("强化特殊技"):
        return AttackKind.SpecialEx
    elif name.startswith("连携技"):
        return AttackKind.Chain
    elif name.startswith("终结技"):
        return AttackKind.Final
    return AttackKind.All


def encode_skill_mark(skills: list[dict]) -> dict[str, dict]:
    name_suffixes = ["", "", "X", "Y", "Z", "U", "V", "W", "x", "y", "z", "u", "v", "w"]
    hit_suffixes = ["", "", "H", "J", "K", "L", "N", "M", "h", "j", "k", "l", "n", "m"]
    prefixes = {
        AttackKind.Basic: "A",
        AttackKind.Dash: "Dash",
        AttackKind.Dodge: "Dodge",
        AttackKind.QuickAssit: "QAssit",
        AttackKind.DefenseAssit: "DAssit",
        AttackKind.Assit: "Assit",
        AttackKind.Special: "E",
        AttackKind.SpecialEx: "EX",
        AttackKind.Chain: "Chain",
        AttackKind.Final: "Final",
        AttackKind.All: "Unknown",
    }

    @dataclass
    class HitInfo:
        index_of_name: int = 0
        derived_count: int = 0  # 蓄力，派生

    @dataclass
    class NameInfo:
        index_of_kind: int = 0
        hits: dict[int, HitInfo] = field(default_factory=dict)

    @dataclass
    class KindInfo:
        total_hits: int = 0
        names: dict[str, NameInfo] = field(default_factory=dict)

    # kind -> { skill-name -> SkillInfo }
    skills_by_kind: dict[AttackKind, KindInfo] = {}

    for skill in skills:
        name = skill["name"]
        cn_index = skill["index"]

        kind = map_atk_kind(name)
        kind_info = skills_by_kind.get(kind, KindInfo())
        kind_info.total_hits += 1
        skills_by_kind[kind] = kind_info

        name_info = kind_info.names.get(
            name, NameInfo(index_of_kind=len(kind_info.names) + 1)
        )
        kind_info.names[name] = name_info

        index = map_cn_index(cn_index)
        if 0 == index:
            index = len(name_info.hits) + 1
        hit_info = name_info.hits.get(index, HitInfo(index_of_name=index))
        hit_info.derived_count += 1
        name_info.hits[index] = hit_info

        mark = ""
        if kind == AttackKind.Basic:
            mark = f"{prefixes.get(kind)}{name_suffixes[name_info.index_of_kind]}{hit_info.index_of_name}{hit_suffixes[hit_info.derived_count]}"
        else:
            mark = f"{prefixes.get(kind)}{kind_info.total_hits}{hit_suffixes[hit_info.derived_count]}"

        skill["kind"] = kind
        skill["mark"] = mark

    # debug = [(t["name"] + "-" + t["index"], t["mark"]) for t in skills]
    # import pprint

    # pprint.pprint(debug)

    # debug = [t["mark"] for t in skills]
    # for m in debug:
    #     print(f'{m} = "{m}"')

    return {skill["mark"]: skill for skill in skills}


@lru_cache
def load_skills() -> dict[str, dict[str, dict]]:
    result: dict[str, dict[str, dict]] = {}
    skills: dict[str, list[dict]] = {}

    with open(directory + "/skills.csv", encoding="utf-8") as file:
        spamreader = csv.reader(file, delimiter="\t")
        header = True
        for line, row in enumerate(spamreader):
            if header:
                header = False
                continue
            if not row:
                continue
            agent = row[0]

            item = {}
            item["agent"] = agent
            item["line"] = line
            item["name"] = row[1]
            item["index"] = row[2]
            item["full_name"] = row[1] + "-" + row[2]
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

            agent_skills = skills.get(agent, [])
            skills[agent] = agent_skills
            agent_skills.append(item)

        for agent, agent_skill in skills.items():
            result[agent] = encode_skill_mark(agent_skill)

    return result


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
