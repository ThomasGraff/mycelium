<template>
  <v-card class="position-relative">
    <v-card-title>Data Contracts List</v-card-title>
    <v-card-text>
      <!-- Tableau pour afficher la liste des data contracts -->
      <v-data-table
        :items="dataContracts"
        :headers="headers"
        item-value="id"
        class="elevation-1"
      >
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      // Liste des data contracts
      dataContracts: [],
      // Définition des colonnes pour l'affichage
      headers: [
        { title: 'Title', value: 'info.title' },
        { title: 'Version', value: 'info.version' },
        { title: 'Description', value: 'info.description' },
        { title: 'Owner', value: 'info.owner' },
        { title: 'Status', value: 'info.status' }
      ]
    }
  },
  methods: {
    async fetchDataContracts () {
      try {
        // Requête GET pour récupérer les data contracts depuis l'API
        const response = await axios.get('http://127.0.0.1:8000/data_contract/')
        // Vérifie si la clé 'data' contient un tableau avant de l'assigner
        if (Array.isArray(response.data.data)) {
          this.dataContracts = response.data.data
        } else {
          console.error('Data contracts API did not return a list')
        }
      } catch (error) {
        console.error('Error fetching data contracts:', error)
      }
    }
  },
  created () {
    // Récupère les data contracts dès que le composant est monté
    this.fetchDataContracts()
  }
}
</script>

<style scoped>
.v-card {
  margin-top: 20px;
  padding: 20px;
}
</style>
