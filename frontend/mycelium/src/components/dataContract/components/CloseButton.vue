<template>
  <v-btn
    icon="mdi-close-thick"
    size="x-small"
    @click="emitCloseEvent"
    class="position-absolute top-0 right-0 clear-button pa-2"
  >
  </v-btn>
</template>

<script setup>
const emit = defineEmits(['close'])

const emitCloseEvent = () => {
  emit('close')
}
</script>

<style scoped>
.v-card {
  margin-top: 20px;
  padding: 20px;
}

.scrollable-card {
  max-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
