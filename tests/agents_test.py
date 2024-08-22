from pyzzz import agents
from pyzzz.model import *


if __name__ == "__main__":
    agent = agents.AgentWithData(
        "Ellen", level=50, skill_levels=SkillLevels(4, 9, 9, 9, 9, 9)
    )
    print(agent)

    agent = agents.AgentWithData("Ellen", level=60)
    print(agent)

    agent = agents.Ellen()
    print(agent)

    agent = agents.Soukaku()
    print(agent)

    agent = agents.Lycaon()
    print(agent)

    agent = agents.Rina()
    print(agent)

    agent = agents.Nekomata()
    print(agent)

    agent = agents.Soldier11()
    print(agent)

    agent = agents.Zhuyuan()
    print(agent)

    agent = agents.Nicole()
    print(agent)

    agent = agents.Jane()
    print(agent)
