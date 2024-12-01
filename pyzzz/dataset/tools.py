import click
import csv
import os
from pathlib import Path

from pyzzz import dataset as db
from pyzzz.dataset import mappings
from pyzzz.model import *

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


@click.command()
def write_agent_csv():
    all = db.load_zzz_gg_agents()

    with open(Path(directory) / "agents_profiles.csv", "w") as f:
        header = [
            "name",
            "camp",
            "profession",
            "attribute",
            "atk_base",
            "atk_growth",
            "hp_base",
            "hp_growth",
            "def_base",
            "def_growth",
            "impact",
            "energy_regen",
            "anomaly_master",
            "anomaly_proficiency",
        ]
        w = csv.DictWriter(f, header)
        w.writeheader()

        for name, agent in all["agents"].items():
            row = {
                "name": name,
                "camp": agent["CampName"],
                "profession": agent["ProfessionName"],
                "attribute": agent["ElementTypeName"],
                "atk_base": agent["Atk"],
                "atk_growth": agent["AttackGrowth"] / 1e4,
                "hp_base": agent["HpMax"],
                "hp_growth": agent["HPGrowth"] / 1e4,
                "def_base": agent["Def"],
                "def_growth": agent["DefenceGrowth"] / 1e4,
                "impact": agent["BreakStun"],
                "energy_regen": agent["SpRecover"] / 1e2,
                "anomaly_master": agent["ElementMystery"],
                "anomaly_proficiency": agent["ElementAbnormalPower"],
            }
            w.writerow(row)

    with open(Path(directory) / "agents_ascensions.csv", "w") as f:
        header = ["name", "rank", "atk", "hp", "def"]
        w = csv.DictWriter(f, header)
        w.writeheader()
        for name, ascs in all["ascensions"].items():
            for rank, asc in list(ascs.items())[1:]:
                row = {
                    "name": name,
                    "rank": rank - 1,
                    "atk": asc["Atk"],
                    "hp": asc["HpMax"],
                    "def": asc["Def"],
                }
                w.writerow(row)

    with open(Path(directory) / "agents_passives.csv", "w") as f:
        header = ["name", "rank", "kind1", "value1", "kind2", "value2"]
        w = csv.DictWriter(f, header)
        w.writeheader()

        def parse_passive(m) -> list[StatValue]:
            result = []
            for k, v in m.items():
                if k == "ATK":
                    result.append(StatValue(v, StatKind.ATK_FLAT))
                elif k == "Impact":
                    result.append(StatValue(v, StatKind.IMPACT))
                elif k == "CRIT Rate":
                    result.append(StatValue(v / 1e4, StatKind.CRIT_RATIO))
                elif k == "CRIT DMG":
                    result.append(StatValue(v / 1e4, StatKind.CRIT_MULTI))
                elif k == "Energy Regen":
                    result.append(StatValue(v / 1e2, StatKind.ENERGY_REGEN))
                elif k == "Anomaly Mastery":
                    result.append(StatValue(v, StatKind.ANOMALY_MASTER))
                elif k == "Anomaly Proficiency":
                    result.append(StatValue(v, StatKind.ANOMALY_PROFICIENCY))
                elif k == "PEN Ratio":
                    result.append(StatValue(v, StatKind.PEN_RATIO))
                else:
                    raise Exception(f"unknown passive item {k} {v}")
            return result

        for name, passives in all["passives"].items():
            for rank, (l, m) in enumerate(passives.items()):
                kvs = parse_passive(m)
                row = {
                    "name": name,
                    "rank": rank,
                    "kind1": str(kvs[0].kind),
                    "value1": kvs[0].value,
                    "kind2": str(kvs[1].kind),
                    "value2": kvs[1].value,
                }
                w.writerow(row)


cli.add_command(write_agent_csv)


@cli.command()
def write_weapon_csv():
    all = db.load_zzz_gg_weapons()
    with open(Path(directory) / "weapons_zeros.csv", "w") as f:
        header = [
            "name",
            "model",
            "profession",
            "atk_base",
            "advanced_kind",
            "advanced_value",
        ]
        w = csv.DictWriter(f, header)
        w.writeheader()
        for name, weapon in all["weapons"].items():
            row = {
                "name": name,
                "model": int(weapon["Rarity"]),
                "profession": weapon["ProfessionName"],
                "atk_base": weapon["BaseProperty"]["Value"],
                "advanced_kind": str(
                    db.ZZZ_GG_STAT_PRIMARY[weapon["RandProperty"]["Name"]]
                ),
                "advanced_value": weapon["RandProperty"]["Value"],
            }
            if "%" in weapon["RandProperty"]["ShowForm"]:
                row["advanced_value"] /= 1e4
            w.writerow(row)

    with open(Path(directory) / "weapons_levelup.csv", "w") as f:
        header = [
            "model",
            "level",
            "atk_rate",
        ]
        w = csv.DictWriter(f, header)
        w.writeheader()
        for model, growth in all["levelings"].items():
            for level, g in enumerate(growth):
                if level == 0:
                    continue
                row = {
                    "model": model,
                    "level": level,
                    "atk_rate": g.atk_rate,
                }
                w.writerow(row)

    with open(Path(directory) / "weapons_ascensions.csv", "w") as f:
        header = [
            "model",
            "rank",
            "atk_rate",
            "advanced_rate",
        ]
        w = csv.DictWriter(f, header)
        w.writeheader()
        for model, ascs in all["ascensions"].items():
            for rank, asc in enumerate(ascs):
                if rank == 0:
                    continue
                row = {
                    "model": model,
                    "rank": rank,
                    "atk_rate": asc.atk_rate,
                    "advanced_rate": asc.primary_rate,
                }
                w.writerow(row)


cli.add_command(write_weapon_csv)


@click.command()
def write_skills_csv():
    total_skills = db.load_skills()
    with open(Path(directory) / "agents_skills.csv", "w") as f:
        header = [
            "agent",
            "mark",
            "cn_agent",
            "cn_skill",
            "kind",
            "dmg_base",
            "dmg_grow",
            "impact_base",
            "impact_grow",
            "energy_gain",
            "decibel_gain",
            "anomaly",
        ]
        w = csv.DictWriter(f, header)
        w.writeheader()
        for agent_skills in total_skills.values():
            for mark, skill in agent_skills.items():
                row = {
                    "agent": skill.agent,
                    "mark": mark,
                    "cn_agent": skill.cn_agent,
                    "cn_skill": skill.cn_hit_name,
                    "kind": skill.kind,
                    "dmg_base": round(skill.dmg_base, 6),
                    "dmg_grow": round(skill.dmg_grow, 6),
                    "impact_base": round(skill.impact_base, 6),
                    "impact_grow": round(skill.impact_grow, 6),
                    "energy_gain": round(skill.energy_gain, 6),
                    "decibel_gain": round(skill.decibel_gain, 6),
                    "anomaly": round(skill.anomaly, 6),
                }
                w.writerow(row)


cli.add_command(write_skills_csv)


if __name__ == "__main__":
    cli()
