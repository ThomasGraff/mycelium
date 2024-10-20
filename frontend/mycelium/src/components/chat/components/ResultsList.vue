<template>
  <div class="results">
    <v-container>
      <v-row>
        <v-col cols="12" v-for="(result, index) in reversedResults" :key="index">
          <ResultBox :result="result" :index="index" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ResultBox from './ResultBox.vue'

const results = ref([])

const reversedResults = computed(() => [...results.value].reverse())

const addResult = (newResult) => {
  results.value.push(newResult)
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
  flex-direction: column-reverse;
  max-height: 76vh;
}
</style>
