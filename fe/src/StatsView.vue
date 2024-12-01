
<script setup lang="ts">

type Initial = {
  [key: string]: number,
}

const initial = defineModel<Initial>("initial");

const makeFlat = (v: number) => {
  return v.toFixed(2)
}

const makePct = (v: number) => {
  return (v * 100).toFixed(1) + '%'
}

</script>

<template>
  <div style="margin: 8px;"></div>
  <el-descriptions size="small" border :column="1">
    <el-descriptions-item width="60%" label="ATK"> {{ makeFlat(initial.atk ?? 0) }} </el-descriptions-item>
    <el-descriptions-item width="60%" label="CRIT RATIO"> {{ makePct(initial.crit_ratio ?? 0) }} </el-descriptions-item>
    <el-descriptions-item width="60%" label="CRIT MUTLI"> {{ makePct(initial.crit_multi ?? 0) }}</el-descriptions-item>

    <el-descriptions-item width="60%" label="DMG RATIO"> {{ makePct(initial.dmg_ratio ?? 0) }}</el-descriptions-item>
    <el-descriptions-item width="60%" label="PEN RATIO"> {{ makePct(initial.pen_ratio ?? 0) }}</el-descriptions-item>
    <el-descriptions-item width="60%" label="PEN FLAT"> {{ makeFlat(initial.pen_flat ?? 0) }}</el-descriptions-item>

    <el-descriptions-item width="60%" label="AM"> {{ makeFlat(initial.anomaly_master ?? 0) }}</el-descriptions-item>
    <el-descriptions-item width="60%" label="AP"> {{ makeFlat(initial.anomaly_proficiency ?? 0) }}</el-descriptions-item>
  </el-descriptions>
  <div style="margin: 6px;"></div>
  <el-descriptions size="small" border :column="1">
    <el-descriptions-item width="60%" label="HP"> {{ makeFlat(initial.hp ?? 0) }}</el-descriptions-item>
    <el-descriptions-item width="60%" label="DEF"> {{ makeFlat(initial.defense ?? 0) }}</el-descriptions-item>
    <el-descriptions-item width="60%" label="IMPACT"> {{ makeFlat(initial.impact ?? 0) }}</el-descriptions-item>
    <el-descriptions-item width="60%" label="ENERGE"> {{ makeFlat(initial.energy_regen ?? 0) }}</el-descriptions-item>
  </el-descriptions>
  <div style="margin: 8px;"></div>

</template>