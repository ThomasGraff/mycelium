<template>
  <div class="search-bar">
    <v-form @submit.prevent="search">
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="query"
              append-inner-icon="mdi-magnify"
              variant="outlined"
              label="Search or type 'new' to create..."
              class="search-input"
              clearable
              @keyup.enter="search"
              @click:append-inner="search"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const query = ref('')
const emit = defineEmits(['search'])

const search = () => {
  if (query.value.trim() === '') return
  emit('search', query.value)
  query.value = ''
}
</script>
