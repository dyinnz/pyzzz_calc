from pyzzz.agents.agent import Agent
from pyzzz.agents.ellen import Ellen
from pyzzz.agents.lycaon import Lycaon
from pyzzz.agents.soukaku import Soukaku


def create_agent(name: str, **kw):
    return {
        "Ellen": Ellen,
        "Lycaon": Lycaon,
        "Soukaku": Soukaku,
    }[
        name
    ](**kw)
