<template>
    <div class="chat-column">
      <!-- Barre de recherche -->
       <v-container class="main-container">
        <v-row>
            <!-- ClearButton en haut à droite -->
            <ClearButton @clear-results="handleClearResults" />
            <!-- Résultats de la recherche -->
            <ResultsList ref="resultsList" />
        </v-row>
    </v-container>
    <v-container >
        <v-row>
            <v-col >
                    <SearchBar @search="handleSearch" />
            </v-col>
        </v-row>
       </v-container>
    </div>
  </template>
<script>
import SearchBar from './SearchBar.vue'
import ResultsList from './ResultsList.vue'
import ClearButton from './ClearButton.vue'

export default {
  components: {
    SearchBar,
    ResultsList,
    ClearButton
  },

  methods: {
    handleClearResults () {
      // Accède à l'instance du composant ResultsList et appelle sa méthode clearResults
      this.$refs.resultsList.clearResults()
    },
    handleSearch (search) {
      if (search.toLowerCase() === 'new') {
        this.$emit('showDataContract', true)
      }
      this.$refs.resultsList.addResult(search)
    }

  }
}

</script>

<style scoped>

.chat-column {
  display: flex;
  flex-direction: column;
  height: 88vh; /* Prend la hauteur de la fenêtre */
}

.main-container {
  flex: 1; /* Remplit l'espace disponible */
  display: flex;
  flex-direction: column;
}

.search-bar {
  margin-top: auto; /* Pousse la barre de recherche vers le bas */
}
</style>
