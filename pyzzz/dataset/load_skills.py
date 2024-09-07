from pyzzz.model import *
from pyzzz.dataset import mappings
from functools import lru_cache
from dataclasses import dataclass

import os
import csv

file_path = os.path.realpath(__file__)
directory = os.path.dirname(file_path)


@dataclass
class SkillData:
    agent: str = ""
    mark: str = ""
    qualified: str = ""
    kind: AttackKind = AttackKind.All
    cn_agent: str = ""
    cn_name: str = ""
    cn_index: str = ""
    cn_hit_name: str = ""
    dmg_base: float = 0.0
    dmg_grow: float = 0.0
    impact_base: float = 0.0
    impact_grow: float = 0.0
    energy_gain: float = 0.0
    decibel_gain: float = 0.0
    anomaly: float = 0.0
    distance: str = ""

    def pretty(self) -> str:
        return f"{self.qualified: <20}{self.cn_agent:<6}\t{self.cn_hit_name}"


def get_percent(s):
    return float(s[:-1]) / 100


def map_cn_index(name):
    if name.startswith("一段"):
        return 1
    if name.startswith("二段"):
        return 2
    if name.startswith("三段"):
        return 3
    if name.startswith("四段"):
        return 4
    if name.startswith("五段"):
        return 5
    if name.startswith("六段"):
        return 6
    if name.startswith("七段"):
        return 7
    if name.startswith("八段"):
        return 8
    if name.startswith("九段"):
        return 9
    return 0


def map_atk_kind(name):
    if name.startswith("普通攻击"):
        return AttackKind.Basic
    elif name.startswith("冲刺攻击"):
        return AttackKind.Dash
    elif name.startswith("闪避反击"):
        return AttackKind.Dodge
    elif name.startswith("快速支援"):
        return AttackKind.QuickAssit
    elif name.startswith("招架支援"):
        return AttackKind.DefenseAssit
    elif name.startswith("支援突击"):
        return AttackKind.Assit
    elif name.startswith("特殊技"):
        return AttackKind.Special
    elif name.startswith("强化特殊技"):
        return AttackKind.SpecialEx
    elif name.startswith("连携技"):
        return AttackKind.Chain
    elif name.startswith("终结技"):
        return AttackKind.Final
    return AttackKind.All


def encode_skill_mark(skills: list[SkillData]) -> dict[str, SkillData]:
    name_suffixes = ["", "", "X", "Y", "Z", "U", "V", "W", "x", "y", "z", "u", "v", "w"]
    hit_suffixes = ["", "", "H", "J", "K", "L", "N", "M", "h", "j", "k", "l", "n", "m"]
    prefixes = {
        AttackKind.Basic: "A",
        AttackKind.Dash: "Dash",
        AttackKind.Dodge: "Dodge",
        AttackKind.QuickAssit: "QAssit",
        AttackKind.DefenseAssit: "DAssit",
        AttackKind.Assit: "Assit",
        AttackKind.Special: "E",
        AttackKind.SpecialEx: "EX",
        AttackKind.Chain: "Chain",
        AttackKind.Final: "Final",
        AttackKind.All: "NIL",
    }

    @dataclass
    class HitInfo:
        index_of_name: int = 0
        derived_count: int = 0  # 蓄力，派生

    @dataclass
    class NameInfo:
        index_of_kind: int = 0
        hits: dict[int, HitInfo] = field(default_factory=dict)

    @dataclass
    class KindInfo:
        total_hits: int = 0
        names: dict[str, NameInfo] = field(default_factory=dict)

    # kind -> { skill-name -> SkillInfo }
    skills_by_kind: dict[AttackKind, KindInfo] = {}

    for skill in skills:
        cn_name = skill.cn_name
        cn_index = skill.cn_index

        kind = map_atk_kind(cn_name)
        kind_info = skills_by_kind.get(kind, KindInfo())
        kind_info.total_hits += 1
        skills_by_kind[kind] = kind_info

        name_info = kind_info.names.get(
            cn_name, NameInfo(index_of_kind=len(kind_info.names) + 1)
        )
        kind_info.names[cn_name] = name_info

        index = map_cn_index(cn_index)
        if 0 == index:
            index = len(name_info.hits) + 1
        hit_info = name_info.hits.get(index, HitInfo(index_of_name=index))
        hit_info.derived_count += 1
        name_info.hits[index] = hit_info

        mark = ""
        if kind == AttackKind.Basic:
            mark = f"{prefixes.get(kind)}{name_suffixes[name_info.index_of_kind]}{hit_info.index_of_name}{hit_suffixes[hit_info.derived_count]}"
        else:
            mark = f"{prefixes.get(kind)}{kind_info.total_hits}{hit_suffixes[hit_info.derived_count]}"

        skill.kind = kind
        skill.mark = mark
        skill.qualified = f"{skill.agent}.{skill.mark}"

    return {skill.mark: skill for skill in skills}


@lru_cache
def load_skills() -> dict[str, dict[str, SkillData]]:
    """{ agent -> { mark -> skill-data } }"""

    result: dict[str, dict[str, SkillData]] = {}
    skills: dict[str, list[SkillData]] = {}

    with open(directory + "/skills.csv", encoding="utf-8") as file:
        spamreader = csv.reader(file, delimiter="\t")
        header = True
        for row in spamreader:
            if header:
                header = False
                continue
            if not row:
                continue
            agent = row[0]

            data = SkillData()
            data.agent = mappings.AGENTS_CN2EN[agent]
            data.cn_agent = agent
            data.cn_name = row[1]
            data.cn_index = row[2]
            data.cn_hit_name = row[1] + "-" + row[2] if row[2] else row[1]
            data.dmg_base = get_percent(row[3])
            data.dmg_grow = get_percent(row[4])
            data.impact_base = get_percent(row[5])
            data.impact_grow = get_percent(row[6])
            data.energy_gain = get_percent(row[7])
            data.decibel_gain = float(row[8])
            data.anomaly = float(row[9])
            data.distance = row[10] if len(row) > 10 else ""

            skills[agent] = skills.get(agent, [])
            skills[agent].append(data)

        for agent, agent_skills in skills.items():
            result[agent] = encode_skill_mark(agent_skills)

    return result
