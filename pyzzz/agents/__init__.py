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
    }


def create_agent(name: str, **kw):
    return get_agents_mapping()[name](**kw)


def list_agents():
    res = []
    map = get_agents_mapping()
    for t in map.values():
        agent = t()
        res.append(
            {"name": agent.name, "cn_name": agent.cn_name, "attribute": agent.attribute}
        )
    res.sort(key=lambda x: (x['attribute'], x['name']))
    return res
