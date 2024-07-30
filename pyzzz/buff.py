import copy

from model import ContextData, StatKind, StatValue


class Buff:

    def __init__(self, stat: StatValue, **kw):
        self.stat = stat
        self.source = kw.get("source", "")
        self.cov = kw.get("cov", 1.0)
        self.duration = kw.get("duration", 0.0)  # zero for static buf

    def produce(self, context: ContextData):
        if self.active(context):
            return StatValue(self.stat.value * self.cov, self.stat.kind)
        return StatValue.empty()

    def active(self, _: ContextData):
        return True

    def coverage(self):
        return self.cov

    def __str__(self):
        return f"{self.stat} from '{self.source}'"


WeaponBuff = Buff(StatValue(0.075, StatKind.ATK_PERCENT), source="weapon")
ATKBuff = Buff(StatValue(840, StatKind.ATK_FLAT), source="flat")

Suit4DMGPercent = Buff(StatValue(0.4, StatKind.DMG_PERCENT), cov=0.75, source="suit4")
PartnerDMGPercent = Buff(StatValue(0.2, StatKind.DMG_PERCENT), source="partener")
CoreSkillDMGPercent = Buff(StatValue(0.833, StatKind.CRIT_MULTI), source="core skill")
