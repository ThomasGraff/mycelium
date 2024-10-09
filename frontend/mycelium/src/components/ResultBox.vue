<template>
    <div class="result-box">
      <div v-if="result.type === 'response'">
        <p>{{ result.text }}</p>
      </div>
      <div v-else-if="result.type === 'form'">
        <form @submit.prevent="submit">
          <v-text-field
            v-model="formData" 
            label="Form input"
            clearable
          />
          <v-btn type="submit" color="green">Submit</v-btn> <!-- Ajout d'une couleur -->
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      result: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        formData: this.result.formData || '', // Créez une data locale pour gérer les entrées de formulaire
      };
    },
    methods: {
      submit() {
        // Émet l'événement de soumission avec les données
        this.$emit('submit-form', {
          ...this.result,
          text: `Form submitted with data: ${this.formData}`,
          type: 'response',
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .result-box {
    background-color: #f0f0f0; /* Couleur de fond */
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
    width: 80%; /* Largeur du box */
  }
  </style>
  