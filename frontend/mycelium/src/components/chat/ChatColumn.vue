<template>
  <div class="chat-column">
    <v-container class="main-container">
      <v-row>
        <v-col>
          <!-- Search results -->
          <ResultsList ref="resultsList" />
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row>
        <v-col>
          <SearchBar @search="handleSearch" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue'
import ResultsList from './components/ResultsList.vue'

export default {
  name: 'ChatColumn',
  components: {
    SearchBar,
    ResultsList
  },
  methods: {
    handleSearch (search) {
      const lowerCaseSearch = search.toLowerCase()

      // Logic to determine which object to display
      switch (lowerCaseSearch) {
        case 'new':
          this.$emit('requestObject', 'DataContract')
          break
        case 'list':
          this.$emit('requestObject', 'ListDataContracts')
          break
        case 'close':
          this.$emit('closeObject')
          break
      }

      this.$refs.resultsList.addResult(search)
    }
  }
}
</script>

<style scoped>
.chat-column {
  display: flex;
  flex-direction: column;
  height: 98vh; /* Takes the height of the window */
}

.main-container {
  flex: 1; /* Fills available space */
  display: flex;
  flex-direction: column;
}

.search-bar {
  margin-top: auto; /* Pushes the search bar to the bottom */
}
</style>
