from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.model import *


class GraceExtraMultiplier(ExtraMultiplier):
    def active(self, anomaly: bool, context: HitContext):
        return anomaly

    def calc(self):
        return 1 + 0.36

    def show(self):
        return "(1 + 0.36)"


class Grace(AgentWithData):
    def __init__(
        self, level=60, skill_levels: SkillLevels | None = None, repetition=0, **kw
    ):
        name = "Grace"
        super().__init__(
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

    # TODO:
    # def A31(self):
    #     value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
    #     return Attack(AttackKind.Basic, Attribute.Physical, value * 0.4, 0)

    # def A32(self):
    #     value = self.a3["dmg"] + self.a3["dmg_grow"] * (self.skill_levels.basic - 1)
    #     return Attack(
    #         AttackKind.Basic, Attribute.Electric, value * 0.6, self.a3["anomaly"] * 0.6
    #     )

    def extra_multiplier(self):
        return [GraceExtraMultiplier()]
