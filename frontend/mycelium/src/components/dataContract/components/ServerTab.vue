<template>
  <v-card flat>
    <v-form ref="serverForm" v-model="valid" @update:modelValue="updateServer">
      <v-text-field v-model="server.name" label="Name" required></v-text-field>
      <v-text-field v-model="server.type" label="Type" required></v-text-field>
      <v-text-field v-model="server.environment" label="Environment" required></v-text-field>
      <v-text-field v-model="server.location" label="Location" required></v-text-field>
      <v-text-field v-model="server.format" label="Format" required></v-text-field>
      <v-text-field v-model="server.delimiter" label="Delimiter" required></v-text-field>
      <v-text-field v-model="server.description" label="Description" required></v-text-field>
      <v-text-field v-model="server.username" label="Username" required></v-text-field>
      <v-text-field v-model="server.passwordSecretId" label="Password Secret ID" required></v-text-field>
    </v-form>
  </v-card>
</template>

<script>
import { defineComponent, ref, watch } from 'vue'

export default defineComponent({
  name: 'ServerTab',
  emits: ['update', 'validate'],
  setup (props, { emit }) {
    const valid = ref(false)
    const server = ref({
      name: '',
      type: '',
      environment: '',
      location: '',
      format: '',
      delimiter: '',
      description: '',
      username: '',
      passwordSecretId: ''
    })

    const updateServer = () => {
      emit('update', { ...server.value })
      emit('validate', valid.value)
    }

    watch(valid, (newValue) => {
      emit('validate', newValue)
    })

    return {
      valid,
      server,
      updateServer
    }
  }
})
</script>

<style scoped>
.v-form {
  display: flex;
  flex-direction: column;
}
</style>
