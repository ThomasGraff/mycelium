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
          <InformationTab @update-info="updateInfo" />
        </v-window-item>
        <v-window-item value="server">
          <ServerTab @update="updateServer" />
        </v-window-item>
      </v-window>
    </v-card-text>
    <v-card-actions>
      <SubmitButton @submitObject="submitObject" :isDisabled="!isValid" />
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import CloseButton from './components/CloseButton.vue'
import InformationTab from './components/InformationTab.vue'
import ServerTab from './components/ServerTab.vue'
import SubmitButton from './components/SubmitButton.vue'
import { useResizeObserver } from '@/composables/useResizeObserver'

const emit = defineEmits(['close-object'])

const tab = ref('information')
const isValid = ref(false)

const updateInfo = (info) => {
  console.log('💡 Info updated:', info)
  // TODO: Implement logic to update the data contract information
}

const updateServer = (server) => {
  console.log('💡 Server updated:', server)
  // TODO: Implement logic to update the server information
}

const submitObject = () => {
  console.log('💡 Object submitted')
  // TODO: Implement logic to submit the data contract
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
  max-height: calc(100vh - 64px); /* Adjust based on your navbar height */
  overflow-y: auto;
}
</style>
