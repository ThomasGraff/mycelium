<template>
  <v-card>
    <v-tabs v-model="activeTab" background-color="primary">
      <v-tab>Information</v-tab>
      <v-tab>Servers</v-tab>
      <v-tab>Models</v-tab>
      <v-tab>Links</v-tab>
      <v-tab>Tags</v-tab>
    </v-tabs>

    <v-tabs-items v-model="activeTab">
      <!-- Onglet Information -->
      <v-tab-item>
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
      </v-tab-item>

      <!-- Les autres onglets seront remplis plus tard -->
      <v-tab-item>
        <v-card flat>.</v-card>
      </v-tab-item>

      <v-tab-item>
        <v-card flat></v-card>
      </v-tab-item>

      <v-tab-item>
        <v-card flat></v-card>
      </v-tab-item>

      <v-tab-item>
        <v-card flat></v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      activeTab: 0, // Onglet actif (commence par Information)
      valid: false, // Validation du formulaire
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
    // Vous pourrez ajouter ici des méthodes pour valider et soumettre le data contract
  }
}
</script>

<style scoped>
.v-card {
  margin-top: 20px;
  padding: 20px;
}
</style>
