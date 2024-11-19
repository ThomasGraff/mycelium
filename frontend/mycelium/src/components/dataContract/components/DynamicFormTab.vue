<template>
    <v-form>
      <div v-for="(field, fieldName) in sectionData" :key="fieldName">
        <!-- Vérifie le type pour afficher un champ d'input -->
        <v-text-field
          v-if="isStringType(field)"
          v-model="formData[sectionName][fieldName]"
          :label="fieldName"
          @input="updateField(sectionName, fieldName, $event)"
        />
        <!-- Exemple d'autres types de champs si besoin -->
        <v-checkbox
          v-else-if="isBooleanType(field)"
          v-model="formData[sectionName][fieldName]"
          :label="fieldName"
          @input="updateField(sectionName, fieldName, $event)"
        />
        <!-- Ajoutez ici des champs supplémentaires pour d'autres types -->

        <!-- Recurssion pour les objets imbriqués -->
        <template v-else-if="typeof field === 'object' && !Array.isArray(field)">
          <p><strong>{{ fieldName }}</strong></p>
          <DynamicFormTab :sectionData="field" :sectionName="fieldName" />
        </template>
      </div>
    </v-form>
  </template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  sectionData: Object,
  sectionName: String
})
const formData = ref({})

// Détecter le type pour afficher le bon champ
const isStringType = (field) => typeof field === 'string' && field === 'string'
const isBooleanType = (field) => typeof field === 'boolean' || field === 'boolean'

const updateField = (sectionName, fieldName, value) => {
  formData.value[sectionName][fieldName] = value
}

// Initialiser les données du formulaire à chaque changement de sectionData
watch(() => props.sectionData, (newData) => {
  if (!formData.value[props.sectionName]) {
    formData.value[props.sectionName] = {}
  }
  Object.keys(newData).forEach(key => {
    formData.value[props.sectionName][key] = newData[key]
  })
}, { immediate: true })
</script>
