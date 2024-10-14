<template>
  <v-card class="position-relative" >
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
        <InformationTab />
      </v-tabs-window-item>

      <!-- Onglet Servers -->
      <v-tabs-window-item value="1">
        <ServerTab />
      </v-tabs-window-item>

      <!-- Onglets restants (pour plus tard) -->
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
  </v-card>
</template>

<script>
import InformationTab from './components/InformationTab.vue'
import ServerTab from './components/ServerTab.vue'
import CloseButton from './components/CloseButton.vue'

export default {
  components: {
    InformationTab,
    ServerTab,
    CloseButton
  },
  data () {
    return {
      activeTab: 0, // Onglet actif, par défaut "Information"
      valid: false // Validation des formulaires
    }
  },
  methods: {
    handleCloseObject () {
      // Accède à l'instance du composant ResultsList et appelle sa méthode clearResults
      this.$emit('showDataContract', false)
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
