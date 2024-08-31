<script setup lang="ts">

import { EnemyModel } from './model';

const enemy = defineModel<EnemyModel>();

</script>

<template>
  <div>
    <el-row class="enemy-row" :gutter="8">
      <el-col :span="6" class="enemy-text">
        <el-text > Level </el-text>
      </el-col>
      <el-col :span="6">
        <el-input-number v-model="enemy.level" :min="1" :max="70" controls-position="right" style="width: 100%;">
        </el-input-number>
      </el-col>
      <el-col :span="6" class="enemy-text">
        <el-text> Defense Base </el-text>
      </el-col>
      <el-col :span="6">
        <el-input-number v-model="enemy.base" :min="36" :max="60" controls-position="right" style="width: 100%;">
        </el-input-number>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="css" scoped>
.enemy-text {
  display: flex;
  justify-content: center;
  text-align: center;
}
.enemy-row {
  margin-bottom: 20px;
  margin-top: 3px;
}
</style>