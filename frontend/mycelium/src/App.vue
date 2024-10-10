<template>
  <v-app>
    <!-- NavBar -->
    <NavBar />

    <!-- ClearButton en haut à droite -->
    <ClearButton @clear-results="clearResults" />

    <!-- Contenu principal -->
    <v-main>
      <SearchBar @search="handleSearch" />
      <ResultsList
        :results="results"
        @submit-form="submitForm"
      />
    </v-main>
  </v-app>
</template>

<script>
import NavBar from './components/NavBar.vue'
import SearchBar from './components/SearchBar.vue'
import ResultsList from './components/ResultsList.vue'
import ClearButton from './components/ClearButton.vue' // Ajout du ClearButton

export default {
  components: {
    NavBar,
    SearchBar,
    ResultsList,
    ClearButton // Ajout du ClearButton dans les composants
  },
  data () {
    return {
      results: [] // Tableau pour stocker les résultats
    }
  },
  methods: {
    handleSearch (query) {
      if (query.toLowerCase() === 'new') {
        this.results.push({ type: 'datacontract' }) // Ajoute un DataContract
      } else {
        this.results.push({ type: 'response', text: query }) // Ajoute une réponse
      }
    },
    submitForm (index, updatedResult) {
      // Mettez à jour le tableau de résultats avec le nouveau résultat
      this.$set(this.results, index, updatedResult) // Utilisez $set pour une réactivité appropriée
    },
    clearResults () {
      this.results = [] // Vide le tableau des résultats
    }
  }
}
</script>

<style>
#app {
  text-align: center;
}
</style>
