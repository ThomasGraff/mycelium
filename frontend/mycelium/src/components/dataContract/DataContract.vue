<template>
  <v-card class="scrollable-card">
    <v-card-title>
      Data Contract
      <CloseButton @close="closeObject" />
    </v-card-title>
    <v-tabs v-model="tab" background-color="primary">
      <v-tab value="information">Information</v-tab>
      <v-tab value="server">Server</v-tab>
    </v-tabs>
    <v-card-text>
      <v-window v-model="tab">
        <v-window-item value="information">
          <InformationTab @update-info="updateInfo" @validate="validateInformation" />
        </v-window-item>
        <v-window-item value="server">
          <ServerTab @update="updateServer" @validate="validateServer" />
        </v-window-item>
      </v-window>
    </v-card-text>
    <v-card-actions class="submit-button-container">
      <SubmitButton @submitObject="submitObject" :isDisabled="!isValid" />
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import CloseButton from './components/CloseButton.vue'
import InformationTab from './components/InformationTab.vue'
import ServerTab from './components/ServerTab.vue'
import SubmitButton from './components/SubmitButton.vue'
import { useResizeObserver } from '@/composables/useResizeObserver'
import axios from 'axios'

const emit = defineEmits(['close-object', 'contract-added'])

const tab = ref('information')
const informationValid = ref(false)
const serverValid = ref(false)
const informationTab = ref({})
const serverTab = ref({})

const isValid = computed(() => informationValid.value && serverValid.value)

const updateInfo = (info) => {
  console.log('💡 Info updated:', info)
  informationTab.value = info
}

const updateServer = (server) => {
  console.log('💡 Server updated:', server)
  serverTab.value = server
}

const validateInformation = (valid) => {
  informationValid.value = valid
}

const validateServer = (valid) => {
  serverValid.value = valid
}

const submitObject = async () => {
  try {
    const dataContract = {
      info: informationTab.value,
      server: serverTab.value
    }
    const response = await axios.post('http://127.0.0.1:8000/data_contract/', dataContract)
    console.log('💡 Data contract submitted successfully:', response.data)
    emit('contract-added')
    emit('close-object')
  } catch (error) {
    console.error('❌ Error submitting data contract:', error)
  }
}

const closeObject = () => {
  console.log('💡 Close object')
  emit('close-object')
}

useResizeObserver('.v-window-item')

// ResizeObserver error workaround
const resizeObserverHandler = (entries) => {
  for (const entry of entries) {
    if (entry.target.clientHeight === 0) {
      return
    }
  }
}

let resizeObserver
onMounted(() => {
  resizeObserver = new ResizeObserver(resizeObserverHandler)
  document.querySelectorAll('.v-window-item').forEach(el => {
    resizeObserver.observe(el)
  })
})

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})
</script>

<style scoped>
.scrollable-card {
  max-height: calc(100vh - 64px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.submit-button-container {
  display: flex;
  justify-content: center;
  padding: 16px 0;
}
</style>
