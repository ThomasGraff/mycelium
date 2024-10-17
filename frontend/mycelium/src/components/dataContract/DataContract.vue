<template>
  <v-card class="position-relative">
    <CloseButton @closeObject="handleCloseObject" />
    <!-- Onglets -->
    <v-tabs v-model="activeTab" background-color="primary">
      <v-tab value="0">Information</v-tab>
      <v-tab value="1">Servers</v-tab>
      <v-tab value="2">Models</v-tab>
      <v-tab value="3">Links</v-tab>
      <v-tab value="4">Tags</v-tab>
    </v-tabs>

    <!-- Contenu des onglets -->
    <v-tabs-window v-model="activeTab" class="overflow">
      <!-- Onglet Information -->
      <v-tabs-window-item value="0">
        <InformationTab @update-info="updateDataContractInfo" />
      </v-tabs-window-item>

      <!-- Onglet Servers -->
      <v-tabs-window-item value="1">
        <ServerTab />
      </v-tabs-window-item>

      <!-- Onglets restants -->
      <v-tabs-window-item value="2">
        <v-card flat></v-card>
      </v-tabs-window-item>

      <v-tabs-window-item value="3">
        <v-card flat></v-card>
      </v-tabs-window-item>

      <v-tabs-window-item value="4">
        <v-card flat></v-card>
      </v-tabs-window-item>

      <v-tabs-window-item value="5">
        <v-card flat></v-card>
      </v-tabs-window-item>
    </v-tabs-window>

    <SubmitButton @submitObject="handleSubmitObject" />
  </v-card>
</template>

<script>
import InformationTab from './components/InformationTab.vue'
import ServerTab from './components/ServerTab.vue'
import CloseButton from './components/CloseButton.vue'
import SubmitButton from './components/SubmitButton.vue'
import axios from 'axios'

export default {
  components: {
    InformationTab,
    ServerTab,
    CloseButton,
    SubmitButton
  },
  data () {
    return {
      activeTab: 0, // Onglet actif, par défaut "Information"
      valid: false, // Validation des formulaires
      dataContract: {
        dataContractSpecification: '0.9.3', // Valeur par défaut pour data_contract_specification
        id: 'urn:datacontract:example', // Valeur par défaut pour l'ID
        info: {
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
    }
  },
  methods: {
    handleCloseObject () {
      this.$emit('showDataContract', false)
    },
    handleSubmitObject () {
      this.submitDataContract()
    },
    updateDataContractInfo (info) {
      // Mettre à jour les informations dans dataContract quand l'enfant émet update-info
      this.dataContract.info = info
    },

    async submitDataContract () {
      try {
        // Envoi de la requête POST à l'API
        console.log('test')
        const response = await axios.post('http://localhost:8000/data-contracts/', this.dataContract)
        console.log('Response received:', response) // Ajoutez cette ligne
        console.log('Data contract created successfully:', response.data)

        // Affichage d'une notification de succès
        this.$notify({
          title: 'Succès',
          message: 'Le contrat de données a été créé avec succès!',
          type: 'success'
        })

        // Réinitialiser ou rediriger l'utilisateur, si nécessaire
        // this.resetForm(); // Exemple de fonction pour réinitialiser le formulaire
      } catch (error) {
        // Gérer les erreurs d'API
        console.error('Error creating data contract:', error.response ? error.response.data : error.message)

        // Affichage d'une notification d'erreur
        this.$notify({
          title: 'Erreur',
          message: error.response ? error.response.data.message : 'Une erreur s\'est produite lors de la création du contrat de données.',
          type: 'error'
        })
      } finally {
    console.log('Finished submitDataContract') // Cela s'affichera à chaque fois
    }
  }
}
}
</script>

<style scoped>
.v-card {
  margin-top: 20px;
  padding: 20px;
  flex: 1; /* Remplit l'espace disponible */
  display: flex;
  flex-direction: column;
}

.overflow {
  max-height: calc(100vh - 200px); /* Ajustez cette valeur selon votre besoin */
  overflow: auto;
}
</style>
