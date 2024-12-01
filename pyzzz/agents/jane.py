from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.model import *
from pyzzz.buff import DynamicBuff


class JaneExtraMultiplier(ExtraMultiplier):
    def __init__(self, agent: AgentWithData):
        self.agent = agent

    @property
    def crit_ratio(self):
        base = [0.2, 0.25, 0.28, 0.31, 0.34, 0.37, 0.4][self.agent.skill_levels.core]
        multi = [0.0010, 0.0011, 0.0012, 0.0013, 0.0014, 0.0015, 0.0016][
            self.agent.skill_levels.core
        ]
        return min(base + multi * self.agent.dynamic.calc_ap(), 1.0)

    def active(self, anomaly: bool, context: HitContext):
        return anomaly

    def calc(self):
        return 1 + self.crit_ratio * 0.5

    def show(self):
        return (
            f"(1 + {self.crit_ratio:.4f} * 0.5) # Jane anomaly extra criti multiplier"
        )


class Jane(AgentWithData):
    def __init__(
        self,
        level=60,
        is_ascension=False,
        skill_levels: SkillLevels | None = None,
        repetition=0,
        **kw,
    ):
        name = "Jane"
        super().__init__(
            name=name,
            level=level,
            is_ascension=is_ascension,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

    def passion_stream(self):
        def create():
            value = (self.dynamic.calc_ap() - 120) * 2
            value = min(value, 600)
            value = max(0, value)
            return StatValue(value, StatKind.ATK_FLAT)

        return DynamicBuff(
            create,
            owner=self.name,
            source="passion stream atk",
            priority=100,
        )

    def buffs(self):
        return [self.passion_stream()]

    def extra_multiplier(self):
        return [JaneExtraMultiplier(self)]
