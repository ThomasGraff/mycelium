<template>
  <div>
    <NavBar
      @new-chat="handleNewChat"
      @create-data-contract="handleCreateDataContract"
      @list-data-contracts="handleListDataContracts"
    />
    <v-main>
      <v-container color="#2f2f2f">
        <v-row :class="{ 'object-open': isObjectVisible }">
          <v-col :cols="isObjectVisible ? 6 : 12" class="search-results-column">
            <ChatColumn
              ref="chatColumn"
              @request-object="handleObjectRequest"
              @close-object="closeObject"
            />
          </v-col>

          <v-col v-if="isObjectVisible" cols="6">
            <component
              :is="currentObjectComponent"
              @close-object="closeObject"
              @contract-added="handleContractAdded"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import NavBar from '@/components/navigation/NavBar.vue'
import DataContract from '@/components/dataContract/DataContract.vue'
import ListDataContracts from '@/components/listDataContracts/ListDataContracts.vue'
import ChatColumn from '@/components/chat/ChatColumn.vue'

export default defineComponent({
  name: 'HomePage',
  components: {
    NavBar,
    DataContract,
    ListDataContracts,
    ChatColumn
  },
  setup () {
    const isObjectVisible = ref(false)
    const currentObjectComponent = ref(null)
    const chatColumn = ref(null)

    const searchResultsColumnClass = computed(() => ({
      'search-results-column': true,
      'object-open': isObjectVisible.value
    }))

    const handleObjectRequest = (objectType) => {
      isObjectVisible.value = true
      currentObjectComponent.value = objectType
    }

    const closeObject = () => {
      isObjectVisible.value = false
      currentObjectComponent.value = null
    }

    const handleNewChat = () => {
      closeObject()
      chatColumn.value.clearChat()
    }

    const handleCreateDataContract = () => {
      handleObjectRequest('DataContract')
    }

    const handleListDataContracts = () => {
      handleObjectRequest('ListDataContracts')
    }

    const handleContractAdded = () => {
      // If ListDataContracts is currently visible, refresh it
      if (currentObjectComponent.value === 'ListDataContracts') {
        // Assuming ListDataContracts has a method to refresh its data
        this.$refs.listDataContracts.fetchDataContracts()
      }
    }

    return {
      isObjectVisible,
      currentObjectComponent,
      searchResultsColumnClass,
      handleObjectRequest,
      closeObject,
      handleNewChat,
      handleCreateDataContract,
      handleListDataContracts,
      chatColumn,
      handleContractAdded
    }
  }
})
</script>

<style scoped>
.object-open .search-results-column {
  text-align: left;
}

.search-results-column {
  text-align: center;
}
</style>
