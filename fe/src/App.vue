<script lang="ts" setup>

import { computed } from "vue";
import { ref } from "vue";
import About from "./About.vue";
import Calc from "./Calc.vue";

const index = ref<string>("/calc")
const handleSelect = (idx: string) => {
  index.value = idx;
}

const routes = {
  '/about': About,
  '/calc': Calc,
}
const currentView = computed(() => {
  // @ts-ignore
  return routes[index.value]
})
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="100px">
        <el-menu @select="handleSelect" default-active="/calc">
          <el-menu-item index="/agents" disabled>
            <span>Agents</span>
          </el-menu-item>
          <el-menu-item index="/discs" disabled>
            <span>Discs</span>
          </el-menu-item>
          <el-menu-item index="/calc">
            <span>Calc</span>
          </el-menu-item>
          <el-menu-item index="/about">
            <span>About</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <component :is="currentView" />
      </el-main>
    </el-container>
  </div>
</template>