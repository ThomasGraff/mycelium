<template>
    <div class="search-bar">
      <v-text-field
        v-model="query"
        variant="outlined"
        label="Search or type 'new' to create..."
        @keyup.enter="search"
        class="search-input"
        clearable
      >
        <template v-slot:append-inner>
          <v-icon
            @click="search" 
            class="validate-button"
          >
            mdi-magnify
          </v-icon>
        </template>
      </v-text-field>
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
        if (this.query.trim() === '') return; // Ne rien faire si la requête est vide
        this.$emit('search', this.query);
        this.query = ''; // Réinitialiser après la soumission
      },
    },
  };
  </script>
  
  <style scoped>
  .search-bar {
    display: flex;
    justify-content: center;  
    position: fixed;          
    left: 50%;                
    bottom: 20px;            
    transform: translate(-50%, 0); 
    width: 100%;             
  }
  
  .search-input {
    width: 400px;            
    max-width: 80%;         
  }
  </style>
  