<script setup lang="ts">
import type { StatValue } from './model'
const stat = defineModel<StatValue>();
const props = defineProps({
  primary: Boolean
});
</script>

<template>
  <el-row justify="center">
    <el-text style="font-size: 13px;">
      {{ stat.kind ? stat.kind : "empty" }} +{{ stat.value }}
    </el-text>
  </el-row>
</template>