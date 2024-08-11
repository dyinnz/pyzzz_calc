from pprint import pprint

from pyzzz import dataset

# from context import pyzzz


# agents_basic = dataset.load_agents_basic()
# pprint.pprint(agents_basic)
#
# skills = dataset.load_skills()
# pprint.pprint(skills)
#
# weapons = dataset.load_weapons()
# pprint.pprint(weapons)


def remove_skills_talents(agent):
    agent.pop("Skills")
    agent.pop("Talents")
    return agent


js = dataset.load_zzz_gg()

agents_list = js["characters"]
for agent in agents_list:
    remove_skills_talents(agent)
id2name = {agent["ID"]: agent["Name"] for agent in agents_list}
agents_dict = {agent["Name"]: agent for agent in agents_list}


# agents_by_id = {agent["ID"]: agent for agent in agents_list}
pprint(agents_dict)

ascension_list = js["ascension"]
ascension_dict = {}
for ascension in ascension_list:
    id = ascension["AvatarID"]
    if id not in id2name:
        continue

    name = id2name[id]
    rank = ascension["Rank"]
    agent_asc = ascension_dict.get(name, {})
    agent_asc[rank] = ascension
    ascension_dict[name] = agent_asc
pprint(ascension_dict)


properties_list = js["properties"]
properties_by_id = {prop["PropID"]: prop for prop in properties_list}
pprint(properties_by_id)
# fix strange id
properties_by_id[20101] = properties_by_id[201]
properties_by_id[21101] = properties_by_id[211]
properties_by_id[23101] = properties_by_id[231]


passive_list = js["passives"]
passive_dict = {}
for passive in passive_list:
    id = passive["AvatarID"]
    if id not in id2name:
        continue

    extra = passive["Extra"]
    props = {
        properties_by_id[prop["Property"]]["Name"]: prop["Value"] for prop in extra
    }

    name = id2name[id]
    max_level = passive["MaxLevel"]
    agent_passive = passive_dict.get(name, {})
    agent_passive[max_level] = props
    passive_dict[name] = agent_passive
pprint(passive_dict)
