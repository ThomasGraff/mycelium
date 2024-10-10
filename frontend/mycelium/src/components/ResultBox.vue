<template>
  <div class="result-box">
    <!-- Si le résultat est une réponse -->
    <div v-if="result.type === 'response'">
      <p>{{ result.text }}</p>
    </div>

    <!-- Si le résultat est un formulaire -->
    <div v-else-if="result.type === 'form'">
      <form @submit.prevent="submit">
        <v-text-field
          v-model="formData"
          label="Form input"
          clearable
        />
        <v-btn type="submit" color="green">Submit</v-btn>
      </form>
    </div>

    <!-- Si le résultat est un data contract -->
    <div v-else-if="result.type === 'datacontract'">
      <DataContract />
    </div>
  </div>
</template>

<script>
import DataContract from './DataContract.vue' // Import du composant DataContract

export default {
  props: {
    result: {
      type: Object,
      required: true
    }
  },
  components: {
    DataContract // Ajout du DataContract comme composant
  },
  data () {
    return {
      formData: this.result.formData || '' // Gérer les entrées de formulaire
    }
  },
  methods: {
    submit () {
      // Émet l'événement de soumission avec les données
      this.$emit('submit-form', {
        ...this.result,
        text: `Form submitted with data: ${this.formData}`,
        type: 'response'
      })
    }
  }
}
</script>

<style scoped>
.result-box {
  background-color: #f0f0f0;
  border-radius: 5px;
  padding: 10px;
  margin: 5px;
  width: 80%;
}
</style>
