<template>
    <v-btn @click="clearResults" class="clear-button" style="background-color: #41B883; color: white;">
      Clear All
    </v-btn>
  </template>
  
  <script>
  export default {
    methods: {
      clearResults() {
        this.$emit('clear-results');
      },
    },
  };
  </script>
  
  <style scoped>
  .clear-button {
    margin: 10px; /* Espace entre la NavBar et le bouton Clear All */
    position: absolute; /* Pour le positionner en haut à droite */
    top: 70px; /* Ajustez selon la hauteur de votre NavBar */
    right: 20px; /* Ajustez selon votre design */
  }
  </style>
  