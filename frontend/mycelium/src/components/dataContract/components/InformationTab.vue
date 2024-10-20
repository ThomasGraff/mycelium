<template>
  <v-card flat>
    <v-form ref="infoForm" v-model="valid" @input="updateInfo">
      <v-text-field v-model="info.title" label="Title" required></v-text-field>
      <v-text-field v-model="info.version" label="Version" required></v-text-field>
      <v-textarea v-model="info.description" label="Description" required></v-textarea>
      <v-text-field v-model="info.owner" label="Owner" required></v-text-field>
      <v-text-field v-model="info.contactName" label="Contact Name" required></v-text-field>
      <v-text-field v-model="info.contactEmail" label="Contact Email" required></v-text-field>
      <v-text-field v-model="info.contactUrl" label="Contact URL"></v-text-field>
      <v-text-field v-model="info.businessUnit" label="Business Unit" required></v-text-field>
    </v-form>
  </v-card>
</template>

<script>
export default {
  name: 'InformationTab',
  data () {
    return {
      info: {
        title: '',
        version: '',
        description: '',
        owner: '',
        contactName: '',
        contactEmail: '',
        contactUrl: '',
        businessUnit: ''
      },
      valid: false
    }
  },
  methods: {
    updateInfo () {
      // Emit the updated information to the parent component
      this.$emit('update-info', { ...this.info })
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
