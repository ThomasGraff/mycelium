<template>
    <v-card flat>
          <v-form ref="infoForm" v-model="valid">
            <v-text-field v-model="dataContract.title" label="Title" required></v-text-field>
            <v-text-field v-model="dataContract.version" label="Version" required></v-text-field>
            <v-textarea v-model="dataContract.description" label="Description" required></v-textarea>
            <v-text-field v-model="dataContract.owner" label="Owner" required></v-text-field>
            <v-text-field v-model="dataContract.contactName" label="Contact Name" required></v-text-field>
            <v-text-field v-model="dataContract.contactEmail" label="Contact Email" required></v-text-field>
            <v-text-field v-model="dataContract.contactUrl" label="Contact URL"></v-text-field>
            <v-text-field v-model="dataContract.businessUnit" label="Business Unit" required></v-text-field>
          </v-form>
        </v-card>
  </template>

<script>
export default {
  data () {
    return {
      dataContract: {
        title: '',
        version: '',
        description: '',
        owner: '',
        contactName: '',
        contactEmail: '',
        contactUrl: '',
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
