from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.buff import StaticBuff
from pyzzz.model import (
    Attribute,
    HitContext,
    SkillLevels,
    StatKind,
    StatValue,
)


class Lycaon(AgentWithData):
    def __init__(
        self, level=60, skill_levels: SkillLevels | None = None, repetition=0, **kw
    ):
        name = "Lycaon"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

        self._cn_name = "莱卡恩"
        self.load_cn_data(self._cn_name)

    def core_skill(self):
        return StaticBuff(
            StatValue(-0.25, StatKind.RES_RATIO),
            condition=HitContext(atk_attr=Attribute.Ice),
            for_team=True,
            source=f"{self._name} core skill Ice DMG RES",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.35, StatKind.STUN_DMG_RATIO),
            condition=HitContext(daze=True),
            for_team=True,
            source=f"{self._name} extra skill Stun DMG Multiplier",
        )

    def buffs(self, _: bool = True):
        return [self.core_skill(), self.extra_skill()]
