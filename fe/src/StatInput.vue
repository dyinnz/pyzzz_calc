<script setup lang="ts">

import type { StatValue } from './model'
import constants from './constants.js';

defineProps(['title'])

const stat = defineModel<StatValue>()

</script>

<template>
  <el-row :gutter="5">
    <el-col :span="8">
      <el-text>{{ title }} </el-text>
    </el-col>
    <el-col :span="8">
      <el-select v-model="stat.kind">
        <el-option v-for="item in constants.discPrimaries" :value="item.value" :label="item.label" />
      </el-select>
    </el-col>
    <el-col :span="8">
      <el-input-number v-model="stat.value" placeholder="0.0" :controls="false" />
    </el-col>
  </el-row>
</template>