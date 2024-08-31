<script setup lang="ts">

import StatInput from './StatInput.vue';
import constants from './constants';
import type { Disc } from './model';
const disc = defineModel<Disc>();

</script>

<template>
  <el-row>
    <h3>Disc Index - {{ disc.index }}</h3>
  </el-row>
  <el-row>
    <el-col :span="12">
      <el-text>Disc Suit</el-text>
    </el-col>
    <el-col :span="12">
      <el-select v-model="disc.kind">
        <el-option v-for="item in constants.discSuits" :value="item" />
      </el-select>
    </el-col>
  </el-row>
  <StatInput title="Primary Stat" v-model="disc.primary" />
  <br/>
  <StatInput title="Secondary Stat" v-model="disc.secondaries[0]" />
  <StatInput title="Secondary Stat" v-model="disc.secondaries[1]" />
  <StatInput title="Secondary Stat" v-model="disc.secondaries[2]" />
  <StatInput title="Secondary Stat" v-model="disc.secondaries[3]" />

</template>