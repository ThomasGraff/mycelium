<template>
  <div class="results">
    <v-container>
      <v-row>
        <v-col cols="12" v-for="(result, index) in results" :key="index">
          <ResultBox :result="result.message" :isUser="result.isUser" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ResultBox from './ResultBox.vue'

const results = ref([])

const addResult = (newResult, isUser = false) => {
  results.value.push({ message: newResult, isUser })
}

const clearResults = () => {
  results.value = []
}

defineExpose({ addResult, clearResults })
</script>

<style scoped>
.results {
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  max-height: 76vh;
  padding: 16px;
}
</style>
