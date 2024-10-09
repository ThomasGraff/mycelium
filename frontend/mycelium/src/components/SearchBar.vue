<!-- src/components/SearchBar.vue -->
<template>
    <div class="search-bar">
      <input
        type="text"
        v-model="query"
        placeholder="Search or type 'new' to create..."
      />
      <button @click="search">Valider</button> <!-- Ajout du bouton Valider -->
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        query: '',
      };
    },
    methods: {
      search() {
        if (this.query.trim()) {
          this.$emit('search', this.query);
          this.query = ''; // Réinitialiser la barre de recherche après la soumission
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .search-bar {
    margin-top: 80px; /* Ajustez cette valeur selon la hauteur de votre navbar */
    display: flex; /* Utilisation de Flexbox pour aligner l'input et le bouton */
    justify-content: center; /* Centrer horizontalement */
    transition: transform 0.3s ease;
  }
  
  .search-bar input {
    padding: 10px;
    font-size: 16px;
    width: 300px; /* Largeur de la barre de recherche */
    margin-right: 10px; /* Espace entre l'input et le bouton */
  }
  
  button {
    padding: 10px 15px; /* Padding pour le bouton */
    background-color: #42b983; /* Couleur Vue.js */
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer; /* Curseur pointer pour indiquer que c'est cliquable */
  }
  
  button:hover {
    background-color: #369f73; /* Couleur du bouton au survol */
  }
  </style>
  