<script lang="ts" setup>
import instance from "./axios";

import { ref } from "vue";
import { onMounted } from "vue";

import { AgentBuild, BuffOperations, EnemyModel, TeamModel } from "./model";
import EnemyInput from './EnemyInput.vue';
import Build from './Build.vue';

import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'

const agentList = ref([]);
const weaponList = ref([]);

const agent1 = ref<AgentBuild>(new AgentBuild);
const agent2 = ref<AgentBuild>(new AgentBuild);
const agent3 = ref<AgentBuild>(new AgentBuild);
const enemy = ref<EnemyModel>(new EnemyModel);

const select1 = ref<string>("");
const select2 = ref<string>("");
const select3 = ref<string>("");
let team = new TeamModel;

const buildList = ref<Array<string>>([]);
const teamList = ref<Array<string>>([]);

const selectedTeam = ref<string>("");
const saveAsTeam = ref<string>("");
const saveAsDialog = ref<boolean>(false);

const editBuffDialog = ref<boolean>(false);
const buffCov = ref<number>(1.0);
let currentBuffKey = { key: "", row: 0 };

const initials = ref([{}, {}, {}]);
const hits = ref([]);
const deltas = ref([]);
const buffs= ref([]);

const loadAgent = (r: any, s: any, id: string) => {
  if (id.length <= 0) {
    r.value = new AgentBuild;
  } else {
    const agentStr = localStorage.getItem(id);
    if (agentStr) {
      r.value = JSON.parse(agentStr)
    }
  }
  s.value = r.value.id;
}

const onTeamChanged = (id: string) => {
  const got = localStorage.getItem(id);
  if (!got) {
    return;
  }
  function reviver(key: string, value: any) {
  if(typeof value === 'object' && value !== null) {
    if (value.dataType === 'Map') {
      return new Map(value.value);
    }
  }
  return value;
}

  const parsedTeam = JSON.parse(got, reviver);
  team.id = parsedTeam.id;
  team.agent1 = parsedTeam.agent1;
  team.agent2 = parsedTeam.agent2;
  team.agent3 = parsedTeam.agent3;
  team.enemy = parsedTeam.enemy;
  team.buffs = parsedTeam.buffs;
  console.log('parsed team buffs', parsedTeam.buffs)

  enemy.value = team.enemy;
  loadAgent(agent1, select1, team.agent1);
  loadAgent(agent2, select2, team.agent2);
  loadAgent(agent3, select3, team.agent3);
  
  console.log(team);
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

  const selectedTeamStr = localStorage.getItem("selectedTeam");
  if (selectedTeamStr) {
    selectedTeam.value = selectedTeamStr;
    onTeamChanged(selectedTeam.value);
  }

  const bl = localStorage.getItem("buildList");
  if (bl) {
    console.log(bl);
    buildList.value = JSON.parse(bl)
  }

  const tl = localStorage.getItem("teamList");
  if (tl) {
    console.log(tl);
    teamList.value = JSON.parse(tl)
  }

  const lastTeamStr = localStorage.getItem("lastTeam");
  if (lastTeamStr) {
    selectedTeam.value = lastTeamStr;
    onTeamChanged(lastTeamStr);
  }
});

const saveImpl = (id: string) => {
  if (id.length <= 0) {
    return 0;
  }
  team.agent1 = agent1.value.id;
  team.agent2 = agent2.value.id;
  team.agent3 = agent3.value.id;
  team.enemy = enemy.value;

  function replacer(key : string, value: any) {
    if (value instanceof Map) {
      return {
        dataType: 'Map',
        value: Array.from(value.entries()), // or with spread: value: [...value]
      };
    } else {
      return value;
    }
  }

  console.log(JSON.stringify(team, replacer))

  localStorage.setItem(id, JSON.stringify(team, replacer));
  localStorage.setItem("lastTeam", id);
}

const onSaveAs = () => {
  if (selectedTeam.value.length > 0) {
    saveAsTeam.value = selectedTeam.value;
  }
  saveAsDialog.value = true;
}

const onSaveAsConfirm = () => {
  saveAsDialog.value = false;
  const id = saveAsTeam.value;
  if (id.length <= 0) {
    return
  }
  if (!teamList.value.includes(id)) {
    let set = (new Set(teamList.value)).add(id);
    let list = [...set].sort()
    localStorage.setItem("teamList", JSON.stringify(list));
    teamList.value = list;
  }
  saveImpl(id);
  selectedTeam.value = id;
}

const onSave = () => {
  if (selectedTeam.value.length <= 0) {
    return;
  }
  saveImpl(selectedTeam.value);
}

const onDelete = () => {
  const id = selectedTeam.value;
  if (id.length <= 0) {
    return;
  }

  const index = teamList.value.indexOf(id);
  if (index > -1) {
    teamList.value.splice(index, 1);
    localStorage.setItem("teamList", JSON.stringify(teamList.value));
  }

  localStorage.removeItem(id);
  selectedTeam.value = "";
}

const makeInput = () => {
  return {
    agent1: agent1.value,
    agent2: agent2.value,
    agent3: agent3.value,
    enemy: enemy.value,
    buffs: Object.fromEntries(team.buffs),
  }
}

const handleCalc = () => {
  const data = makeInput();

  console.log(data.buffs)

  instance
    .put("/calc", data)
    .then((r) => {
      const result = r.data;
      hits.value = result.hit_dmgs
      deltas.value = result.delta_dmgs
      initials.value = result.initials
      buffs.value = result.buffs

      console.log('handleCalc', result.buffs)
      console.log('handleCalc', team.buffs)

      for (let b of buffs.value) {
        if (team.buffs && team.buffs.has(b.key)) {
          b.cov = team.buffs.get(b.key).cov;
        }
      }
    })
    .catch((e) => {
      console.log(e);
    });
}

const handleReset = () => {
  agent1.value = new AgentBuild
  agent2.value = new AgentBuild
  agent3.value = new AgentBuild
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

const onEditBuff = (idx: number, row: any, reset: boolean) => {
  console.log(row.key);
  if (reset) {
    team.buffs.delete(row.key);
    row.cov = row.origin_cov;
  } else {
    currentBuffKey.key = row.key;
    currentBuffKey.row = idx;
    editBuffDialog.value = true;
  }
}

const onBuffCovConfirm = () => {
  let op = new BuffOperations
  op.cov = buffCov.value
  buffs.value[currentBuffKey.row].cov = buffCov.value

  team.buffs.set(currentBuffKey.key, op)
  console.log(team.buffs)

  editBuffDialog.value = false;
}

</script>

<template>
  <el-tabs>
    <el-tab-pane :label="agent1.agent_name ? agent1.agent_name : '队长'">
      <Build v-model:build="agent1" v-model:selected-name="select1" v-model:build-list="buildList"
        v-model:initial="initials[0]" :agent-list="agentList" :weapon-list="weaponList">
      </Build>
    </el-tab-pane>
    <el-tab-pane :label="agent2.agent_name ? agent2.agent_name : '队员'">
      <Build v-model:build="agent2" v-model:selected-name="select2" v-model:build-list="buildList"
        v-model:initial="initials[1]" :agent-list="agentList" :weapon-list="weaponList">
      </Build>
    </el-tab-pane>
    <el-tab-pane :label="agent3.agent_name ? agent3.agent_name : '队员'">
      <Build v-model:build="agent3" v-model:selected-name="select3" v-model:build-list="buildList"
        v-model:initial="initials[2]" :agent-list="agentList" :weapon-list="weaponList">
      </Build>
    </el-tab-pane>
    <el-tab-pane label="敌人">
      <EnemyInput v-model="enemy" />
    </el-tab-pane>
  </el-tabs>

  <el-divider style="margin-top: 10px; margin-bottom: 0px;" />

  <div>
    <el-row :gutter="20">
      <el-col :span="17">
        <h4 style="margin-block-start: 0.5em; margin-block-end: 0.8em;"> Team Calc </h4>
        <el-row justify="center">
          <el-col :span="8">
            <el-button @click="handleReset"> Reset </el-button>
          </el-col>

          <el-col :span="8">
            <el-button type="primary" @click="handleCalc"> Calc </el-button>
          </el-col>
        </el-row>
      </el-col>

      <el-col :span="7">
        <div style="margin: 10px;"></div>
        <el-row :gutter="8">
          <el-select v-model="selectedTeam" @change="onTeamChanged">
            <el-option v-for="item in teamList" :label="item" :value="item" />
          </el-select>
        </el-row>
        <el-row :gutter="5" justify="center">
          <el-col :span="6">
            <el-button @click="onDelete" type="danger" :icon="Delete" style="width: 80%;"></el-button>
          </el-col>
          <el-col :span="9">
            <el-button @click="onSaveAs" style="width: 100%;"> Save As </el-button>
          </el-col>
          <el-col :span="9" justify="space-around">
            <el-button type="primary" @click="onSave" style="width: 100%;"> Save </el-button>
          </el-col>
        </el-row>

        <el-dialog v-model="saveAsDialog">
          <h4>Input agent build name</h4>
          <el-input v-model="saveAsTeam" placeholder="Please input" />
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="saveAsDialog = false; saveAsTeam = ''">Cancel</el-button>
              <el-button type="primary" @click="onSaveAsConfirm">
                Confirm
              </el-button>
            </div>
          </template>
        </el-dialog>

      </el-col>
    </el-row>
  </div>

  <el-tabs value="Hit DMG">
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

    <el-tab-pane label="Buffs">
      <el-table :data="buffs" style="width: 100%">
        <el-table-column label="Edit" width="140px">
          <template #default="scope">
            <el-button size="small" @click="onEditBuff(scope.$index, scope.row, false)">
              Edit
            </el-button>
            <el-button size="small" @click="onEditBuff(scope.$index, scope.row, true)">
              Reset
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="idx" label="Scope" width="70px" />
        <el-table-column prop="stat_str" label="Stat" width="160px" />
        <el-table-column prop="cov" label="Cov" width="60px" />
        <el-table-column prop="key" label="Name" width="300px" />
      </el-table>

      <el-dialog v-model="editBuffDialog">
        <el-input-number v-model="buffCov" :min="0" :max="10000" />
        <div class="dialog-footer">
          <el-button type="primary" @click="onBuffCovConfirm">
            Confirm
          </el-button>
        </div>
      </el-dialog>

    </el-tab-pane>

    <!-- <el-tab-pane label="Multiplier">Multiplier</el-tab-pane> -->
  </el-tabs>
</template>