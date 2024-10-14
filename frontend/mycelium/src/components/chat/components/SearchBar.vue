<template>
    <div class="search-bar">
      <v-form @submit.prevent="search">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="query"
                append-inner-icon='mdi-magnify'
                variant="outlined"
                label="Search or type 'new' to create..."
                class="search-input"
                clearable
                @keyup.enter="search"
                @click="search"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </div>
</template>

<script>
export default {
  data () {
    return {
      query: ''
    }
  },

  methods: {
    search () {
      if (this.query.trim() === '') return // Ne rien faire si la requête est vide
      this.$emit('search', this.query)
      this.query = '' // Réinitialiser après la soumission
    }
  }
}
</script>

<style scoped>
</style>
