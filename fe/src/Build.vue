<script setup lang="ts">

import { AgentBuild, StatValue } from "./model";
import DiscsShow from "./DiscsShow.vue";
import SkillInput from "./SkillInput.vue";
import StatsView from './StatsView.vue';
import {ref} from 'vue';

import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'

const build = defineModel<AgentBuild>("build");
const buildList = defineModel<Array<string>>("buildList");
const selectedName = defineModel<string>("selectedName");
const initial = defineModel<{}>("initial");

const props = defineProps({
  agentList: Array<any>,
  weaponList: Array<any>,
})

const saveAsName = ref<string>("");
const saveAsDialog = ref<boolean>(false);

const saveImpl = (id: string) => {
  if (id.length <= 0) {
    return;
  }
  build.value.id = id;
  localStorage.setItem(id, JSON.stringify(build.value));
}

const onSaveAs = () => {
  if (selectedName.value.length > 0) {
    saveAsName.value = selectedName.value;
  }
  saveAsDialog.value = true;
}

const onSaveAsConfirm = () => {
  saveAsDialog.value = false;
  const id = saveAsName.value;
  if (id.length <= 0) {
    return
  }
  if (!buildList.value.includes(id)) {
    let set = (new Set(buildList.value)).add(id);
    let list = [...set].sort()
    localStorage.setItem("buildList", JSON.stringify(list));
    buildList.value = list;
  }
  saveImpl(id);
  selectedName.value = id;
}

const onDelete = () => {
  const id = selectedName.value;
  if (id.length <= 0) {
    return;
  }

  const index = buildList.value.indexOf(id);
  if (index > -1) {
    buildList.value.splice(index, 1);
    localStorage.setItem("buildList", JSON.stringify(buildList.value));
  }

  localStorage.removeItem(id);
  selectedName.value = "";
}

const onBuildChanged = (id: string) => {
  const got = localStorage.getItem(id);
  if (got) {
    build.value = JSON.parse(got)
    console.log(build.value)
  }
}

</script>

<template>
  <el-row :gutter="20" class="build-all">
    <el-col :span="17">
      <el-row class="build-row">
        <el-text class="build-title"> Basic </el-text>
      </el-row>
      <el-row class="build-row" :gutter="8">
        <el-col :span="12">
          <el-select v-model="build.agent_name">
            <el-option v-for="item in props.agentList" :label="item.attribute + ' / ' + item.name" :value="item.name" />
          </el-select>
        </el-col>

        <el-col :span="6">
          <el-select v-model="build.agent_rep">
            <el-option v-for="item in 7" :label="'影画' + (item - 1)" :value="item - 1" />
          </el-select>
        </el-col>

        <el-col :span="6">
          <el-input-number v-model="build.agent_level" :min="1" :max="60" controls-position="right" class="level-input">
          </el-input-number>
        </el-col>
      </el-row>

      <el-row class="build-row">
        <el-col :span="8">
          <SkillInput v-model="build.skills.basic" title="普通攻击" />
        </el-col>
        <el-col :span="8">
          <SkillInput v-model="build.skills.dodge" title="闪 避" />
        </el-col>
        <el-col :span="8">
          <SkillInput v-model="build.skills.assit" title="支 援" />
        </el-col>
      </el-row>
      <el-row class="build-row">
        <el-col :span="8">
          <SkillInput v-model="build.skills.special" title="特殊技" />
        </el-col>
        <el-col :span="8">
          <SkillInput v-model="build.skills.chain" title="连携/终结" />
        </el-col>
        <el-col :span="8">
          <SkillInput v-model="build.skills.core" title="核 心" />
        </el-col>
      </el-row>

      <el-row class="build-row">
        <el-text class="build-title"> Weapon </el-text>
      </el-row>

      <el-row class="build-row" :gutter="8">
        <el-col :span="12">
          <el-select v-model="build.weapon_name">
            <el-option v-for="item in props.weaponList" :label="item.profession + ' / ' + item.name"
              :value="item.name" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="build.weapon_rep">
            <el-option v-for="item in 5" :label="'精炼' + item" :value="item" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-input-number v-model="build.weapon_level" :min="1" :max="60" controls-position="right"
            class="level-input">
          </el-input-number>
        </el-col>
      </el-row>

      <el-row class="build-row">
        <el-text class="build-title"> Discs </el-text>
      </el-row>
      <DiscsShow v-model="build.discs" />
    </el-col>
    <el-col :span="7">

      <el-row>
        <el-select v-model="selectedName" @change="onBuildChanged">
          <el-option v-for="item in buildList" :label="item" :value="item" />
        </el-select>
      </el-row>
      <el-row justify="center" :gutter="5">
        <el-col :span="6">
          <el-button @click="onDelete" type="danger" :icon="Delete" style="width: 80%;"></el-button>
        </el-col>
        <el-col :span="9">
          <el-button @click="onSaveAs" style="width: 100%;"> Save As </el-button>
        </el-col>
        <el-col :span="9">
          <el-button @click="() => saveImpl(selectedName)" type="primary" style="width: 100%;"> Save </el-button>
        </el-col>
      </el-row>

      <el-dialog v-model="saveAsDialog">
        <h4>Input agent build name</h4>
        <el-input v-model="saveAsName" placeholder="Please input" />
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="saveAsDialog = false; saveAsName = ''">Cancel</el-button>
            <el-button type="primary" @click="onSaveAsConfirm">
              Confirm
            </el-button>
          </div>
        </template>
      </el-dialog>

      <StatsView v-model:initial="initial"/>
    </el-col>
  </el-row>

</template>

<style lang="css" scoped>
.build-all {
  /* margin-bottom: 0px; */
}

.build-row {
  margin-bottom: 3px;
  margin-top: 3px;
}

.level-input {
  width: 100%;
}

.build-title {
  height: 25px;
  line-height: 25px;
  font-weight: bold;
}
</style>