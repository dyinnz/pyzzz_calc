import csv
import os
from functools import lru_cache

from pyzzz.model import AgentData, StatValue

file_path = os.path.realpath(__file__)
directory = os.path.dirname(file_path)


def get_percent(s):
    return float(s[:-1]) / 100


@lru_cache
def load_agents_basic():
    agents = {}

    with open(directory + "/agents_basic.csv") as file:
        spamreader = csv.reader(file, delimiter="\t")
        for row in spamreader:
            agent = AgentData()
            agent.name = row[0]
            agent.level = 60
            # agent.hp = float(row[1])
            # agent.atk = float(row[2])
            # agent.defense = float(row[3])
            agent.crit_ratio = get_percent(row[4])
            agent.crit_multi = get_percent(row[5])
            agent.impact = float(row[6])
            agent.attribte_master = float(row[7])
            # anergy limit
            agent.energy_regen = float(row[9])
            agent.anomaiy_proficiency = float(row[10])
            agent.hp = float(row[11])
            agent.atk = float(row[12])
            agent.defense = float(row[13])

            agents[agent.name] = agent

    return agents


@lru_cache
def load_skills():
    skills = {}

    with open(directory + "/skills.csv") as file:
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
            item["anomaiy"] = float(row[9])
            if len(row) > 10:
                item["distance"] = row[10]
            else:
                item["distance"] = ""
            agent_skill[skill_name] = item
            skills[agent] = agent_skill

    return skills


@lru_cache
def load_weapons():
    weapons = {}

    with open(directory + "/weapons.csv") as file:
        spamreader = csv.reader(file, delimiter="\t")

        for row in spamreader:
            if not row:
                continue
            name = row[0]

            weapon = {}
            weapon["name"] = name
            weapon["rank"] = row[1]
            weapon["atk_0"] = row[2]
            weapon["atk"] = row[3]
            weapon["primary"] = StatValue.from_cn(row[4], row[6])
            weapons[name] = weapon

    return weapons
