<template>
    <div class="results">
      <ResultBox
        v-for="(result, index) in results.slice().reverse()"
        :key="index"
        :result="result"
        @submit-form="submitForm(index, $event)"
      />
    </div>
  </template>
  
  <script>
  import ResultBox from './ResultBox.vue';
  
  export default {
    components: {
      ResultBox,
    },
    props: {
      results: {
        type: Array,
        required: true,
      },
    },
    methods: {
      submitForm(index, updatedResult) {
        // Mettez à jour le tableau de résultats avec le nouveau résultat
        this.$emit('submit-form', index, updatedResult);
      },
    },
  };
  </script>
  
  <style scoped>
  .results {
    margin-top: 80px; /* Ajustez cette valeur selon la hauteur de votre NavBar */
    height: calc(100vh - 250px); /* Ajusté pour laisser de la place à la barre de recherche */
    overflow-y: auto; /* Active le défilement vertical */
    padding: 20px;
    display: flex;
    flex-direction: column-reverse; /* Inverse l'ordre des éléments */
    align-items: center; /* Centre les résultats */
  }
  </style>
  