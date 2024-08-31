<script setup lang="ts">
import type { Disc } from './model'
import StatShow from './StatShow.vue';
import DiscInput from './DiscInput.vue';

import { ref } from 'vue';

const visible = ref(false)
const disc = defineModel<Disc>();



</script>

<template>
  <div class="disc-show">
    <el-row class="disc-box">
      <div class="disc-box-half">
        <el-row justify="center">
          <el-text style="font-weight: bold;"> [{{ disc.index }}] {{ disc.kind.replace('_', ' ') }}</el-text>
        </el-row>
        <StatShow v-model="disc.primary" :primary="true" />
        <el-button style="height: 5px;" @click="visible= true"> Modify </el-button>
      </div>
      <div class="disc-box-half">
        <StatShow v-model="disc.secondaries[0]" />
        <StatShow v-model="disc.secondaries[1]" />
        <StatShow v-model="disc.secondaries[2]" />
        <StatShow v-model="disc.secondaries[3]" />
      </div>
    </el-row>
  </div>

  <el-dialog v-model="visible" :width="'600px'">
    <DiscInput v-model="disc" />
    <div class="dialog-footer">
      <el-button type="primary" @click="visible = false">
        Confirm
      </el-button>
    </div>
  </el-dialog>


</template>

<style scoped>
.disc-show {
  width: 99%;
  border: 1px solid var(--el-border-color);
  border-radius: 15px;
  padding-top: 4px;
  padding-bottom: 4px;
}

.disc-box {
  box-sizing: border-box;
  height: 100%;
}

.disc-box-half {
  box-sizing: border-box;
  height: 100%;
  width: 50%;
  text-align: center;
}
</style>