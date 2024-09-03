<script setup lang="ts">

import { AgentBuild } from "./model";
import DiscsShow from "./DiscsShow.vue";
import SkillInput from "./SkillInput.vue";
import {ref} from 'vue';

const build = defineModel<AgentBuild>("build");
const buildList = defineModel<Array<string>>("buildList");

const props = defineProps({
  agentList: Array<any>,
  weaponList: Array<any>,
})

const saveAsName = ref<string>("");
const saveAsDialog = ref<boolean>(false);

const handleSaveAs = () => {
  saveAsDialog.value = false;

  if (saveAsName.value.length > 0) {
    buildList.value.push(saveAsName.value);
    localStorage.setItem("buildList", JSON.stringify(buildList));
    localStorage.setItem(saveAsName.value, JSON.stringify(build.value));
  }
}

</script>

<template>

  <div>
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
          <el-option v-for="item in props.weaponList" :label="item.profession + ' / ' + item.name" :value="item.name" />
        </el-select>
      </el-col>
      <el-col :span="6">
        <el-select v-model="build.weapon_rep">
          <el-option v-for="item in 5" :label="'精炼' + item" :value="item" />
        </el-select>
      </el-col>
      <el-col :span="6">
        <el-input-number v-model="build.weapon_level" :min="1" :max="60" controls-position="right" class="level-input">
        </el-input-number>
      </el-col>
    </el-row>

    <el-row class="build-row">
      <el-text class="build-title"> Discs </el-text>
    </el-row>

    <DiscsShow v-model="build.discs" />

    <el-row>
      <el-col :span="8">
        <el-button @click="saveAsDialog = true"> Save As </el-button>
      </el-col>
      <el-col :span="8">
        <el-select>
          <el-option v-for="item in buildList" :label="item" :value="item" />
        </el-select>
      </el-col>
      <el-col :span="8">
        <el-button> Save </el-button>
      </el-col>
    </el-row>

    <el-dialog v-model="saveAsDialog">
      <h4>Input agent build name</h4>
      <el-input v-model="saveAsName" placeholder="Please input" />
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="saveAsDialog = false; saveAsName = ''">Cancel</el-button>
          <el-button type="primary" @click="handleSaveAs">
            Confirm
          </el-button>
        </div>
      </template>
    </el-dialog>

  </div>


</template>

<style lang="css" scoped>
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