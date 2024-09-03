<script lang="ts" setup>
import instance from "./axios";

import { ref } from "vue";
import { onMounted } from "vue";

import { AgentBuild, EnemyModel } from "./model";
import EnemyInput from './EnemyInput.vue';
import Build from './Build.vue';

const agentList = ref([]);
const weaponList = ref([]);

const build1 = ref<AgentBuild>(new AgentBuild);
const build2 = ref<AgentBuild>(new AgentBuild);
const build3 = ref<AgentBuild>(new AgentBuild);
const enemy = ref<EnemyModel>(new EnemyModel);

const buildList = ref<Array<String>>([]);

const hits = ref([]);
const deltas = ref([])

const makeData = () => {
  return {
    agent1: build1.value,
    agent2: build2.value,
    agent3: build3.value,
    enemy: enemy.value,
  }
}

onMounted(() => {
  instance
    .get("/list_agents")
    .then((r) => {
      agentList.value = r.data;
      // console.log(agentList.value);
    })
    .catch((e) => {
      console.log(e);
    });

  instance
    .get("/list_weapons")
    .then((r) => {
      weaponList.value = r.data;
      // console.log(weaponList.value);
    })
    .catch((e) => {
      console.log(e);
    });


  const s = localStorage.getItem('build');
  if (s) {
    const obj = JSON.parse(s);
    console.log(obj.enemy)
    build1.value = (obj.agent1 as AgentBuild);
    build2.value = (obj.agent2 as AgentBuild);
    build3.value = (obj.agent3 as AgentBuild);
    enemy.value = (obj.enemy as EnemyModel);
  }
});

const handleSave = () => {
  localStorage.setItem('build', JSON.stringify(makeData()));
}

const handleCalc = () => {
  const data = makeData();
  console.log(data);

  instance
    .put("/calc", data)
    .then((r) => {
      const result = r.data;
      hits.value = result.hit_dmgs
      deltas.value = result.delta_dmgs
      console.log(deltas.value)
    })
    .catch((e) => {
      console.log(e);
    });
}

const handleReset = () => {
  build1.value = new AgentBuild
  build2.value = new AgentBuild
  build3.value = new AgentBuild
  enemy.value = new EnemyModel
}

const sortNumber = (a: any, b: any) => {
  const lhs = a.ratio;
  const rhs = b.ratio;
  return lhs - rhs;
}

const printNumber = (row: any, column: any, value: number, index: number) => {
  return (value * 100).toFixed(2) + '%'
}

</script>

<template>
  <div>
    <el-tabs>
      <el-tab-pane :label="build1.agent_name ? build1.agent_name : '队长'">
        <Build v-model:build="build1" v-model:build-list="buildList" :agent-list="agentList" :weapon-list="weaponList">
        </Build>
      </el-tab-pane>
      <el-tab-pane :label="build2.agent_name ? build2.agent_name : '队员'">
        <Build v-model:build="build2" v-model:build-list="buildList" :agent-list="agentList" :weapon-list="weaponList">
        </Build>
      </el-tab-pane>
      <el-tab-pane :label="build3.agent_name ? build3.agent_name : '队员'">
        <Build v-model:build="build3" v-model:build-list="buildList" :agent-list="agentList" :weapon-list="weaponList">
        </Build>
      </el-tab-pane>
      <el-tab-pane label="敌人">
        <EnemyInput v-model="enemy" />
      </el-tab-pane>
    </el-tabs>
  </div>

  <el-row justify="center">
    <el-col :span="8">
      <el-button @click="handleReset"> Reset </el-button>
    </el-col>

    <el-col :span="8">
      <el-button type="primary" @click="handleSave"> Save </el-button>
    </el-col>
    <el-col :span="8">
      <el-button type="primary" @click="handleCalc"> Calc </el-button>
    </el-col>
  </el-row>

  <div>
    <el-tabs>
      <el-tab-pane label="Hit DMG">
        <el-table :data="hits" style="width: 100%">
          <el-table-column prop="name" label="Hit" width="160px" show-overflow-tooltip />
          <el-table-column prop="mark" label="Mark" width="120px" />
          <el-table-column prop="dmg" label="DMG" width="100px" />
          <el-table-column prop="anomaly_acc" label="Anomaly ACC" width="120px" />
          <el-table-column prop="detail" label="Detail" width="180" show-overflow-tooltip />
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="Suggest">
        <el-table :data="deltas" :default-sort="{ prop: 'ratio', order: 'descending' }" style="width: 100%">
          <el-table-column prop="name" label="Item" width="200px" />
          <el-table-column prop="ratio" label="Ratio" sortable :sort-method="sortNumber" :formatter="printNumber"
            width="120px" />
          <el-table-column prop="detail" label="Detail" width="180" show-overflow-tooltip />
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="Multiplier">Multiplier</el-tab-pane>
    </el-tabs>
  </div>
</template>