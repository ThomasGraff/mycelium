<template>
  <div class="chat-column">
    <div class="results-wrapper" ref="resultsWrapper">
      <ResultsList ref="resultsList" />
    </div>
    <div class="search-bar-container">
      <SearchBar ref="searchBar" @search="handleSearch" :disabled="isWaitingResponse" />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, watch, nextTick } from 'vue'
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
    const searchBar = ref(null)
    const isWaitingResponse = ref(false)

    const getHelpMessage = () => {
      return `Here are the available commands:
* 🆕 **new**: Create a new Data Contract
* 📋 **list**: Display all Data Contracts
* 🚪 **close**: Close the current object
* ❓ **help**: Display this help message`.trim()
    }

    const handleSearch = async (search) => {
      if (isWaitingResponse.value) return

      isWaitingResponse.value = true
      resultsList.value.addResult(search, true)
      resultsList.value.setWaiting(true)

      // Simulate AI response delay
      await new Promise(resolve => setTimeout(resolve, 1000))

      const lowerCaseSearch = search.toLowerCase()
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

      resultsList.value.setWaiting(false)
      resultsList.value.addResult(aiResponse, false)
      isWaitingResponse.value = false

      // Refocus the input after the response is received
      nextTick(() => {
        searchBar.value.focusInput()
      })
    }

    const clearChat = () => {
      resultsList.value.clearResults()
    }

    watch(() => resultsList.value?.results, () => {
      nextTick(() => {
        if (resultsWrapper.value) {
          resultsWrapper.value.scrollTop = resultsWrapper.value.scrollHeight
        }
      })
    }, { deep: true })

    return {
      resultsList,
      resultsWrapper,
      searchBar,
      handleSearch,
      clearChat,
      isWaitingResponse
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
