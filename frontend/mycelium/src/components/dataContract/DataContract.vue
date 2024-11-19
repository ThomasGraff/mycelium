<template>
  <v-card class="scrollable-card">
    <v-card-title>Data Contract <CloseButton @close="closeObject" /></v-card-title>
    <v-tabs v-model="tab" background-color="primary">
      <!-- Onglets dynamiques pour chaque section principale -->
      <v-tab v-for="(tabName, index) in tabNames" :key="index" :value="tabName">
        {{ tabName }}
      </v-tab>
    </v-tabs>
    <v-card-text>
      <v-tabs-window v-model="tab">
        <!-- Afficher chaque section dans un onglet -->
        <v-tabs-window-item v-for="(tabName, index) in tabNames" :key="index" :value="tabName">
          <DynamicFormTab :sectionData="schema[tabName]" :sectionName="tabName" />
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>
    <v-card-actions class="submit-button-container">
      <SubmitButton @submitObject="submitObject" :isDisabled="!isFormValid" />
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import CloseButton from './components/CloseButton.vue'
import SubmitButton from './components/SubmitButton.vue'
import DynamicFormTab from './components/DynamicFormTab.vue' // Nouveau composant pour chaque onglet
import axios from 'axios'

const emit = defineEmits(['close-object', 'contract-added'])

const tab = ref('')
const schema = ref({})
const formData = ref({})
const formValidity = ref({})

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/schema')
    schema.value = response.data

    for (const tabName in schema.value) {
      formData.value[tabName] = {}
      formValidity.value[tabName] = false
    }
    tab.value = Object.keys(schema.value)[0] // Le premier élément est l'onglet par défaut
  } catch (error) {
    console.error('❌ Erreur lors du chargement du schéma:', error)
  }
})

const tabNames = computed(() => {
  return Object.keys(schema.value)
})

const isFormValid = computed(() => {
  return Object.values(formValidity.value).every(valid => valid)
})

const submitObject = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/data_contract/', formData.value)
    console.log('💡 Data contract submitted successfully:', response.data)
    emit('contract-added')
    emit('close-object')
  } catch (error) {
    console.error('❌ Error submitting data contract:', error)
  }
}

const closeObject = () => {
  emit('close-object')
}
</script>

<style scoped>
.scrollable-card {
  max-height: calc(100vh - 64px);
  overflow-y: auto;

  flex-direction: column;
}

.submit-button-container {
  display: flex;
  justify-content: center;
  padding: 16px 0;
}
</style>
