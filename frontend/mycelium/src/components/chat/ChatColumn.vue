<template>
  <div class="chat-column">
    <!-- Barre de recherche -->
    <v-container class="main-container">
      <v-row>
        <v-col>
          <!-- Résultats de la recherche -->
          <ResultsList ref="resultsList" />
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row>
        <v-col>
          <SearchBar @search="handleSearch" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue'
import ResultsList from './components/ResultsList.vue'

export default {
  components: {
    SearchBar,
    ResultsList
  },

  methods: {
    handleSearch (search) {
      const lowerCaseSearch = search.toLowerCase()

      // Logique pour déterminer quel objet afficher
      if (lowerCaseSearch === 'new') {
        this.$emit('requestObject', 'DataContract')
      } else if (lowerCaseSearch === 'list') {
        this.$emit('requestObject', 'ListDataContracts')
      } else if (lowerCaseSearch === 'close') {
        this.$emit('closeObject')
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
  height: 98vh; /* Prend la hauteur de la fenêtre */
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
