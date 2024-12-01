from pyzzz.model import AgentBuild
from pyzzz.weapons import create_weapon
from pyzzz.agent import Agent
from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.agents.ellen import Ellen
from pyzzz.agents.grace import Grace
from pyzzz.agents.lycaon import Lycaon
from pyzzz.agents.soukaku import Soukaku
from pyzzz.agents.rina import Rina
from pyzzz.agents.nekomata import Nekomata
from pyzzz.agents.soldier11 import Soldier11
from pyzzz.agents.zhuyuan import Zhuyuan
from pyzzz.agents.nicole import Nicole
from pyzzz.agents.qingyi import Qingyi
from pyzzz.agents.jane import Jane
from pyzzz.agents.lucy import Lucy
from pyzzz.agents.seth import Seth
from pyzzz.agents.piper import Piper


def get_agents_mapping():
    return {
        "Ellen": Ellen,
        "Lycaon": Lycaon,
        "Soukaku": Soukaku,
        "Grace": Grace,
        "Rina": Rina,
        "Nekomata": Nekomata,
        "Soldier11": Soldier11,
        "Zhu Yuan": Zhuyuan,
        "Nicole": Nicole,
        "Qingyi": Qingyi,
        "Jane": Jane,
        "Lucy": Lucy,
        "Seth": Seth,
        "Piper": Piper,
    }


def create_agent(name: str, **kw) -> Agent:
    return get_agents_mapping()[name](**kw)


def from_agent_build(b: AgentBuild):
    agent = create_agent(
        name=b.agent_name,
        repetition=b.agent_rep,
        level=b.agent_level,
        skill_levels=b.skills,
    )
    weapon = create_weapon(
        name=b.weapon_name,
        repetition=b.weapon_rep,
        level=b.weapon_level,
    )
    agent.set_equipment(weapon=weapon, discs=b.discs)
    return agent


def list_agents():
    res = []
    map = get_agents_mapping()
    for t in map.values():
        agent = t()
        res.append(
            {"name": agent.name, "cn_name": agent.cn_name, "attribute": agent.attribute}
        )
    res.sort(key=lambda x: (x["attribute"], x["name"]))
    return res
