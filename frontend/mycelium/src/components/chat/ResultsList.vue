<template>
  <div class="results">
    <v-container >
      <v-row >
        <v-col cols="12" v-for="(result, index) in results.slice()" :key="index" >
          <ResultBox :result="result" :index="index" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import ResultBox from './ResultBox.vue'

export default {
  data () {
    return {
      results: [] // Tableau pour stocker les résultats
    }
  },
  components: {
    ResultBox
  },
  methods: {
    addResult (newResult) {
      this.results.push(newResult) // Ajoute le nouveau résultat au tableau
    },
    clearResults () {
      this.results = [] // Vide le tableau des résultats
    }
  }
}
</script>

<style scoped>
.results{
  overflow-y: auto;
  flex: 1;
  display: flex; /* Utiliser flexbox */
  flex-direction: column-reverse; /* Positionner les éléments du bas vers le haut */
  max-height: 69vh;
}
</style>
