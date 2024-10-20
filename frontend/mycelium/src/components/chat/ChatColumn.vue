<template>
  <div class="chat-column">
    <div class="results-wrapper" ref="resultsWrapper">
      <ResultsList ref="resultsList" />
    </div>
    <div class="search-bar-container">
      <SearchBar @search="handleSearch" />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, watch } from 'vue'
import SearchBar from './components/SearchBar.vue'
import ResultsList from './components/ResultsList.vue'

export default defineComponent({
  name: 'ChatColumn',
  components: {
    SearchBar,
    ResultsList
  },
  emits: ['requestObject', 'closeObject'],
  setup (props, { emit }) {
    const resultsList = ref(null)
    const resultsWrapper = ref(null)

    const getHelpMessage = () => {
      return `Here are the available commands:
* 🆕 **new**: Create a new Data Contract
* 📋 **list**: Display all Data Contracts
* 🚪 **close**: Close the current object
* ❓ **help**: Display this help message`.trim()
    }

    const handleSearch = (search) => {
      const lowerCaseSearch = search.toLowerCase()

      resultsList.value.addResult(search, true)

      let aiResponse = ''
      switch (lowerCaseSearch) {
        case 'new':
          emit('requestObject', 'DataContract')
          aiResponse = '✨ Creating a new Data Contract. What would you like to add?'
          break
        case 'list':
          emit('requestObject', 'ListDataContracts')
          aiResponse = '📋 Displaying the list of Data Contracts.'
          break
        case 'close':
          emit('closeObject')
          aiResponse = '🚪 Closing the current object.'
          break
        case 'help':
          aiResponse = getHelpMessage()
          break
        default:
          aiResponse = `❓ I'm sorry, I don't understand "${search}".\n\n${getHelpMessage()}`
      }

      setTimeout(() => {
        resultsList.value.addResult(aiResponse, false)
      }, 100)
    }

    const clearChat = () => {
      resultsList.value.clearResults()
    }

    watch(() => resultsList.value?.results, () => {
    }, { deep: true })

    return {
      resultsList,
      resultsWrapper,
      handleSearch,
      clearChat
    }
  }
})
</script>

<style scoped>
.chat-column {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.results-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  padding: 16px;
}

.search-bar-container {
  padding: 16px;
}
</style>
