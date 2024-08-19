from pyzzz.agents.agent import Agent
from pyzzz.agents.ellen import Ellen
from pyzzz.agents.grace import Grace
from pyzzz.agents.lycaon import Lycaon
from pyzzz.agents.soukaku import Soukaku
from pyzzz.agents.rina import Rina
from pyzzz.agents.nekomata import Nekomata
from pyzzz.agents.soldier11 import Soldier11
from pyzzz.agents.zhuyuan import Zhuyuan


def create_agent(name: str, **kw):
    return {
        "Ellen": Ellen,
        "Lycaon": Lycaon,
        "Soukaku": Soukaku,
        "Grace": Grace,
        "Rina": Rina,
        "Nekomata" : Nekomata,
        "Soldier11": Soldier11,
        "Zhuyuan": Zhuyuan,
    }[
        name
    ](**kw)
