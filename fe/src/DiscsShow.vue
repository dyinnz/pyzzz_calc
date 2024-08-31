<script setup lang="ts">

import DiscShow from './DiscShow.vue';
import type { Discs } from './model';

const discs = defineModel<Discs>()

</script>

<template>

  <el-row :gutter="10">
    <el-col :span="12">
      <DiscShow v-model="discs.discs[0]" />
    </el-col>
    <el-col :span="12">
      <DiscShow v-model="discs.discs[5]" />
    </el-col>
    <el-col :span="12">
      <DiscShow v-model="discs.discs[1]" />
    </el-col>
    <el-col :span="12">
      <DiscShow v-model="discs.discs[4]" />
    </el-col>
    <el-col :span="12">
      <DiscShow v-model="discs.discs[2]" />
    </el-col>
    <el-col :span="12">
      <DiscShow v-model="discs.discs[3]" />
    </el-col>
  </el-row>

</template>

<style lang="css" scoped>
.el-col {
  margin-bottom: 8px;
}
</style>