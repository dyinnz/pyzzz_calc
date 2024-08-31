

export class SkillLevels {
  basic: number = 11;
  dodge: number = 11;
  assit: number = 11;
  special: number = 11;
  chain: number = 11;
  core: number = 6;
}

export class StatValue {
  value: number = 0.0;
  kind: string = "empty";
};

export class Disc {
  index: number = 0;
  kind: string = "empty";
  primary: StatValue = new StatValue;
  secondaries: Array<StatValue> = [new StatValue, new StatValue, new StatValue, new StatValue];

  constructor(index: number = 0) {
    this.index = index;
  }
};

export class Discs {
  discs: Array<Disc>

  public get(idx: number): Disc {
    return this.discs[idx]
  }

  constructor() {
    let disc1 = new Disc(1)
    disc1.primary.kind = 'hp_flat'
    disc1.primary.value = 2200

    let disc2 = new Disc(2)
    disc2.primary.kind = 'atk_flat'
    disc2.primary.value = 316

    let disc3 = new Disc(3)
    disc3.primary.kind = 'def_flat'
    disc3.primary.value = 184

    let disc4 = new Disc(4)
    disc4.primary.kind = 'crit_ratio'
    disc4.primary.value = 0.3

    let disc5 = new Disc(5)
    disc5.primary.kind = 'dmg_ratio'
    disc5.primary.value = 0.3

    let disc6 = new Disc(6)
    disc6.primary.kind = 'atk_ratio'
    disc6.primary.value = 0.3

    this.discs = [disc1, disc2, disc3, disc4, disc5, disc6]
  }
}

export class AgentBuild {
  agent_name: string = "";
  agent_rep: number = 0;
  agent_level: number = 60;

  weapon_name: string = "";
  weapon_rep: number = 1;
  weapon_level: number = 60;

  skills: SkillLevels = new SkillLevels;
  discs: Discs = new Discs;
};

export class EnemyModel {
  level: number = 70;
  base: number = 60;
}

export default {
  Stat: StatValue,
  Disc: Disc,
}


