<template>
  <!-- <h1>ZZZ Calculator</h1> -->

  <!-- <el-button>Hello</el-button> -->

  <div class="common-layout">
    <el-container>
      <el-aside width="80px">Aside</el-aside>
      <el-main>
        <div>
          Agent
          <el-select v-model="agentName">
            <el-option
              v-for="item in options"
              :label="item.value"
              :value="item.value"
            />
          </el-select>

          <el-input-number v-model="agentRep" :min="0" :max="6">
          </el-input-number>

          <el-input-number v-model="agentLevel" :min="1" :max="60">
          </el-input-number>

          <el-select v-model="weaponName">
            <el-option
              v-for="item in options"
              :label="item.value"
              :value="item.value"
            />
          </el-select>
          <el-input-number v-model="weaponRep" :min="1" :max="60">
          </el-input-number>

          <el-input-number v-model="weaponLevel" :min="1" :max="60">
          </el-input-number>
        </div>
        <textarea v-model="agentName"></textarea>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";

const agentName = ref("Ellen");
const agentRep = ref(0);
const agentLevel = ref(60);

const weaponName = ref("Ellen");
const weaponRep = ref(0);
const weaponLevel = ref(60);

const options = [
  {
    value: "Ellen",
  },
  {
    value: "Lycaon",
  },
  {
    value: "Soukaku",
  },
];
</script>
