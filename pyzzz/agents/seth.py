from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.buff import DynamicBuff, StaticBuff
from pyzzz.model import (
    SkillLevels,
    StatKind,
    StatValue,
)


class Seth(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=6,
        **kw,
    ):
        name = "Seth"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

    def ap_buff(self):
        def create():
            value = [50, 62, 75, 85, 90, 95, 100][self.skill_levels.core]
            return StatValue(value, StatKind.ANOMALY_PROFICIENCY)

        res = DynamicBuff(
            create,
            owner=self.name,
            source="core skill",
            for_team=True,
        )
        return res

    def ap_res_buff(self):
        return StaticBuff(
            StatValue(0.2, StatKind.ANOMALY_RES),
            owner=self.name,
            source="passive skill",
            for_team=True,
        )

    def buffs(self):
        return [self.ap_buff(), self.ap_res_buff()]
