import click
import os
from pathlib import Path

from pyzzz import dataset as db
from pyzzz.dataset import mappings

file_path = os.path.realpath(__file__)
directory = os.path.dirname(file_path)


@click.group()
def cli():
    pass


@click.command()
def show_skills():
    total_skills = db.load_skills()
    for agent_skills in total_skills.values():
        for skill in agent_skills.values():
            print(skill.pretty())


cli.add_command(show_skills)


@click.command()
def show_agents():
    total_agents = db.load_zzz_gg_agents()["agents"]
    for agent in total_agents.keys():
        print(agent.replace(" ", ""))


cli.add_command(show_agents)


@click.command()
def codegen_agent_marks():
    total_skills = db.load_skills()
    with open(Path(directory) / "marks.py", "w") as f:
        for agent, agent_skills in total_skills.items():
            en = mappings.AGENTS_CN2EN[agent]
            f.write(f"class {en}:\n")
            for mark in agent_skills:
                f.write(f'    {mark} = "{mark}"\n')
            f.write("\n\n")


cli.add_command(codegen_agent_marks)


if __name__ == "__main__":
    cli()
