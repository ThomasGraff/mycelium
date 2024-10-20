<template>
  <v-card class="position-relative">
    <CloseButton @close-object="handleCloseObject" />
    <v-card-title>Data Contracts List</v-card-title>
    <v-card-text>
      <!-- Table to display the list of data contracts -->
      <v-data-table
        :items="dataContracts"
        :headers="headers"
        item-value="id"
        class="elevation-1"
      >
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'
import CloseButton from './components/CloseButton.vue'

export default defineComponent({
  name: 'ListDataContracts',
  components: {
    CloseButton
  },
  emits: ['close-object'],
  setup (props, { emit }) {
    const dataContracts = ref([])
    const headers = [
      { title: 'Title', value: 'info.title' },
      { title: 'Version', value: 'info.version' },
      { title: 'Description', value: 'info.description' },
      { title: 'Owner', value: 'info.owner' },
      { title: 'Status', value: 'info.status' }
    ]

    const handleCloseObject = () => {
      emit('close-object')
    }

    const fetchDataContracts = async () => {
      try {
        // GET request to retrieve data contracts from the API
        const response = await axios.get('http://127.0.0.1:8000/data_contract/')
        // Check if the 'data' key contains an array before assigning it
        if (Array.isArray(response.data.data)) {
          dataContracts.value = response.data.data
        } else {
          console.error('💡 Data contracts API did not return a list')
        }
      } catch (error) {
        console.error('❌ Error fetching data contracts:', error)
      }
    }

    onMounted(() => {
      // Fetch data contracts when the component is mounted
      fetchDataContracts()
    })

    return {
      dataContracts,
      headers,
      handleCloseObject
    }
  }
})
</script>

<style scoped>
.v-card {
  margin-top: 20px;
  padding: 20px;
}
</style>
