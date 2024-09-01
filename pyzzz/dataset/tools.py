import click

from pyzzz.dataset import load_skills


@click.command(name="show_skills")
def show_skills():
    total_skills = load_skills()
    for agent_skills in total_skills.values():
        for skill in agent_skills.values():
            agent = skill["agent"]
            mark = skill["mark"]
            qualified = agent + "." + mark
            full = skill["full_name"]
            print(f"{qualified: <20}\t{full}")


if __name__ == "__main__":
    show_skills()
