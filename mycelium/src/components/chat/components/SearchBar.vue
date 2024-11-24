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
              :disabled="disabled"
              ref="searchInput"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const query = ref('')
const searchInput = ref(null)
const emit = defineEmits(['search'])

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const search = () => {
  if (query.value.trim() === '' || props.disabled) return
  emit('search', query.value)
  query.value = ''
  focusInput()
}

const focusInput = () => {
  nextTick(() => {
    searchInput.value?.focus()
  })
}

onMounted(() => {
  focusInput()
})

defineExpose({ focusInput })
</script>
