import buff
from buff import Buff
from model import AgentData, Disc, DiscKind, DiscList, StatKind, StatValue, WeaponData


class Build:

    def __init__(self):
        self.agent = AgentData(0, 0.0)
        self.weapon = WeaponData(0, 0.0, StatValue.empty())
        self.discs = DiscList([])

        self.buffs = list[Buff]()

    def __str__(self):
        s = f"Build:\n" + f"{self.agent}\n" + f"{self.weapon}\n" + f"{self.discs}\n"
        s += "Buffs:\n"
        for buff in self.buffs:
            s += f"\t{buff}\n"
        return s


def test_build():
    b = Build()
    b.agent.level = 50
    b.agent.atk = 1278
    b.agent.crit_prob = 78.6 / 100
    b.agent.crit_muilti = 69.2 / 100

    disc = Disc(0, DiscKind.Empty, StatValue.empty())
    disc.secondaries.append(
        StatValue(sum([0.3, 0.3, 0.03, 0.09]), StatKind.ATK_PERCENT)
    )
    disc.secondaries.append(StatValue(sum([57, 19, 19, 316]), StatKind.ATK_FLAT))
    disc.secondaries.append(StatValue(sum([0.1]), StatKind.DMG_PERCENT))  # suit2

    b.discs.append(disc)

    b.buffs.append(buff.WeaponBuff)
    b.buffs.append(buff.ATKBuff)
    b.buffs.append(buff.Suit4DMGPercent)
    b.buffs.append(buff.PartnerDMGPercent)
    b.buffs.append(buff.CoreSkillDMGPercent)

    return b


if __name__ == "__main__":
    print(test_build())
