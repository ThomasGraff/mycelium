<template>
  <div class="results" ref="resultsContainer">
    <v-container>
      <v-row>
        <v-col cols="12" v-for="(result, index) in results" :key="index">
          <ResultBox :result="result.message" :isUser="result.isUser" />
        </v-col>
      </v-row>
      <v-row v-if="isWaiting">
        <v-col cols="12">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import ResultBox from './ResultBox.vue'

const results = ref([])
const isWaiting = ref(false)
const resultsContainer = ref(null)

const addResult = (newResult, isUser = false) => {
  results.value.push({ message: newResult, isUser })
  scrollToBottom()
}

const clearResults = () => {
  results.value = []
}

const setWaiting = (waiting) => {
  isWaiting.value = waiting
  if (waiting) {
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (resultsContainer.value) {
      resultsContainer.value.scrollTop = resultsContainer.value.scrollHeight
    }
  })
}

watch(results, () => {
  scrollToBottom()
}, { deep: true })

defineExpose({ addResult, clearResults, setWaiting })
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

.typing-indicator {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 10px;
}

.typing-indicator span {
  height: 10px;
  width: 10px;
  float: left;
  margin: 0 1px;
  background-color: #9E9EA1;
  display: block;
  border-radius: 50%;
  opacity: 0.4;
}

.typing-indicator span:nth-of-type(1) {
  animation: 1s blink infinite 0.3333s;
}

.typing-indicator span:nth-of-type(2) {
  animation: 1s blink infinite 0.6666s;
}

.typing-indicator span:nth-of-type(3) {
  animation: 1s blink infinite 0.9999s;
}

@keyframes blink {
  50% {
    opacity: 1;
  }
}
</style>
