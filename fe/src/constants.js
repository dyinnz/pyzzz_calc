
const discSuits = [
  "fanged_metal",
  "polar_metal",
  "thunder_metal",
  "chaotic_metal",
  "inferno_metal",
  "swing_jazz",
  "soul_rock",
  "hormone_punk",
  "freedom_blues",
  "shockstar_disco",
  "puffer_electro",
  "woodpecker_electro",
]

const discPrimaries = [
  { value: "crit_ratio", label: "CRIT RATIO%" },
  { value: "crit_mutli", label: "CRIT MULTI%" },
  { value: "atk_ratio", label: "ATK RATIO%" },
  { value: "atk_flat", label: "ATK Flat" },
  { value: "dmg_ratio", label: "DMG RATIO%" },
  { value: "pen_ratio", label: "PEN RATIO%" },
  { value: "pen_flat", label: "PEN FLAT" },
  { value: "anomaly_master", label: "异常掌控" },
  { value: "anomaly_proficiency", label: "异常精通" },

  { value: "hp_ratio", label: "HP RATIO%" },
  { value: "hp_flat", label: "HP Flat" },
  { value: "def_ratio", label: "DEF RATIO%" },
  { value: "def_flat", label: "DEF Flat" },
];

const discSecondaries = [
  { value: "crit_ratio", label: "CRIT RATIO%" },
  { value: "crit_mutli", label: "CRIT MULTI%" },
  { value: "atk_ratio", label: "ATK RATIO%" },
  { value: "atk_flat", label: "ATK Flat" },
  { value: "pen_flat", label: "PEN FLAT" },
  { value: "anomaly_proficiency", label: "异常精通" },

  { value: "hp_ratio", label: "HP RATIO%" },
  { value: "hp_flat", label: "HP Flat" },
  { value: "def_ratio", label: "DEF RATIO%" },
  { value: "def_flat", label: "DEF Flat" },
]

export default {
  discPrimaries: discPrimaries,
  discSecondaries: discSecondaries,
  discSuits: discSuits,
}