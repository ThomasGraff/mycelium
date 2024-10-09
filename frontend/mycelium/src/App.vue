<template>
  <v-app>
    <NavBar />
    <v-main>
      <SearchBar @search="handleSearch" @clear="clearResults" />
      <ResultsList
        :results="results"
        @submit-form="submitForm" 
      />
    </v-main>
  </v-app>
</template>

<script>
import NavBar from './components/NavBar.vue';
import SearchBar from './components/SearchBar.vue';
import ResultsList from './components/ResultsList.vue';

export default {
  components: {
    NavBar,
    SearchBar,
    ResultsList,
  },
  data() {
    return {
      results: [], // Tableau pour stocker les résultats
    };
  },
  methods: {
    handleSearch(query) {
      if (query.toLowerCase() === 'new') {
        this.results.push({ type: 'form', formData: '' }); // Ajoute un formulaire
      } else {
        this.results.push({ type: 'response', text: query }); // Ajoute une réponse
      }
    },
    submitForm(index, updatedResult) {
      // Mettez à jour le tableau de résultats avec le nouveau résultat
      this.$set(this.results, index, updatedResult); // Utilisez $set pour une réactivité appropriée
    },
    clearResults() {
      this.results = []; // Vide le tableau des résultats
    },
  },
};
</script>

<style>
#app {
  text-align: center;
}
</style>
