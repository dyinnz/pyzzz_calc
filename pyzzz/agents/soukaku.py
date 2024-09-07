from pyzzz.agents.agent_with_data import AgentWithData
from pyzzz.buff import StaticBuff, DynamicBuff
from pyzzz.model import (
    AttackKind,
    Attribute,
    HitContext,
    SkillLevels,
    StatKind,
    StatValue,
)


class Soukaku(AgentWithData):
    def __init__(
        self,
        level=60,
        skill_levels: SkillLevels | None = None,
        core_skill_atk=None,
        repetition=6,
        **kw,
    ):
        name = "Soukaku"
        AgentWithData.__init__(
            self,
            name=name,
            level=level,
            skill_levels=skill_levels,
            repetition=repetition,
            **kw,
        )

        self.core_skill_atk = int(core_skill_atk) if core_skill_atk else None

    def final_buff(self):
        return StaticBuff(
            StatValue(0.15, StatKind.CRIT_RATIO),
            condition=[
                HitContext(atk_kind=AttackKind.Final, agent=self.name),
                HitContext(atk_kind=AttackKind.Basic, agent=self.name),
                HitContext(atk_kind=AttackKind.Dash, agent=self.name),
            ],
            owner=self.name,
            source="final buff +15% critical ratio",
        )

    def core_skill(self):
        def create():
            m = [0, 12.5, 15, 17, 18, 19, 20][self.skill_levels.core] / 100 * 2
            value = (
                self.core_skill_atk
                if self.core_skill_atk is not None
                else self.initial.atk * m
            )
            value = min(1000, value)
            return StatValue(value, StatKind.ATK_FLAT)

        return DynamicBuff(
            create,
            owner=self.name,
            source="core skill atk dynamic flat",
            for_team=True,
        )

    def extra_skill(self):
        return StaticBuff(
            StatValue(0.2, StatKind.DMG_RATIO),
            condition=HitContext(atk_attr=Attribute.Ice),
            owner=self.name,
            source="extra skill ice dmg ratio",
            for_team=True,
        )

    def rep4(self):
        return StaticBuff(
            StatValue(-0.1, StatKind.RES_RATIO),
            condition=HitContext(atk_attr=Attribute.Ice),
            owner=self.name,
            source="rep4 ice res ratio",
            for_team=True,
        )

    def rep6(self):
        return StaticBuff(
            StatValue(0.45, StatKind.DMG_RATIO),
            condition=[
                HitContext(
                    agent=self.name, atk_attr=Attribute.Ice, atk_kind=AttackKind.Basic
                ),
                HitContext(
                    agent=self.name, atk_attr=Attribute.Ice, atk_kind=AttackKind.Dash
                ),
            ],
            source="rep6 ice dmg ratio",
        )

    def buffs(self):
        res = [self.core_skill(), self.extra_skill(), self.final_buff()]
        if self._repetition >= 4:
            res.append(self.rep4())
        if self._repetition >= 6:
            res.append(self.rep6())
        return res
