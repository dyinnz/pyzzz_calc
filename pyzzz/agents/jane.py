from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.model import *
from pyzzz.buff import DynamicBuff


class JaneExtraMultiplier(ExtraMultiplier):
    def __init__(self, agent: AgentWithData):
        self.agent = agent

    @property
    def crit_ratio(self):
        return min(0.4 + 0.0016 * self.agent.static.anomaly_proficiency, 1.0)

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

        self._cn_name = "简"
        self.load_cn_data(self._cn_name)

    def passion_stream(self):
        def create():
            value = min((self.static.anomaly_proficiency - 120) * 2, 600)
            return StatValue(value, StatKind.ATK_FLAT)

        return DynamicBuff(
            create,
            source=f"{self.name} passion stream atk",
        )

    def buffs(self):
        return [self.passion_stream()]

    def extra_multiplier(self):
        return [JaneExtraMultiplier(self)]
