from pyzzz import agents
from pyzzz.model import *


def all():
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


def new():
    agent = agents.Ellen()
    print(agent)
    # for hit in agent.hit_marks():
    #     print(hit())


if __name__ == "__main__":
    # all()
    new()
