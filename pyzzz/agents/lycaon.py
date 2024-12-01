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

    def core_skill(self):
        return StaticBuff(
            StatValue(-0.25, StatKind.ATTR_RES),
            condition=HitContext(atk_attr=Attribute.Ice),
            for_team=True,
            owner=self.name,
            source="core skill Ice DMG RES",
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.35, StatKind.STUN_DMG_RATIO),
            condition=HitContext(daze=True),
            for_team=True,
            owner=self.name,
            source="extra skill",
        )

    def buffs(self, _: bool = True):
        return [
            self.core_skill(),
            self.extra_skill(),
            StaticBuff(
                StatValue(1000, StatKind.ATK_FLAT),
                for_team=True,
                owner="Caesar",
                source="Caesar 1000 ATK",
            ),
            StaticBuff(
                StatValue(0.20, StatKind.DMG_RATIO),
                for_team=True,
                owner="Caesar",
                source="Caesar 20% DMG",
            ),
        ]
