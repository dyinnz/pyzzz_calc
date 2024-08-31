<script setup lang="ts">

const level = defineModel<number|string>();

const props = defineProps({
  title: String,
})

</script>

<template>
  <div style="display: flex; text-align: center;">
    <el-text style="width: 45%;"> {{ props.title}}&nbsp;</el-text>
    <el-select v-if="props.title === '核 心'" v-model="level" style="width: 55%;">
      <el-option v-for="item in ['A', 'B', 'C', 'D', 'E', 'F']" :label="item"
        :value="item.charCodeAt(0) - 'A'.charCodeAt(0) + 1" />
    </el-select>
    <el-select v-else v-model="level" style="width: 55%;">
      <el-option v-for="item in 16" :label="item" :value="item" />
    </el-select>
  </div>
</template>