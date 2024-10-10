<template>
    <v-form>
      <v-text-field v-model="info.title" label="Titre" required></v-text-field>
      <v-text-field v-model="info.version" label="Version"></v-text-field>
      <v-textarea v-model="info.description" label="Description"></v-textarea>
      <v-text-field v-model="info.responsible" label="Responsable"></v-text-field>
      <v-text-field v-model="info.contactName" label="Nom du contact"></v-text-field>
      <v-text-field v-model="info.contactEmail" label="Email du contact"></v-text-field>
      <v-text-field v-model="info.contactURL" label="URL du contact"></v-text-field>
      <v-text-field v-model="info.businessUnit" label="Unité d'affaire"></v-text-field>

      <v-btn class="mt-4" color="primary" @click="updateInfo">Update Information</v-btn>
    </v-form>
  </template>

<script>
export default {
  data () {
    return {
      info: {
        title: '',
        version: '',
        description: '',
        responsible: '',
        contactName: '',
        contactEmail: '',
        contactURL: '',
        businessUnit: ''
      }
    }
  },
  methods: {
    updateInfo () {
      this.$emit('update', { ...this.info }) // Emit the updated information back to the parent
    }
  }
}
</script>

  <style scoped>
  .v-form {
    display: flex;
    flex-direction: column;
  }
  </style>
