<template>
  <v-btn
    icon="mdi-close-thick"
    size="x-small"
    @click="closeObject"
    class="position-absolute top-0 right-0 clear-button pa-2"
  >
  </v-btn>
</template>

<script>
export default {
  name: 'CloseButton',
  emits: ['closeObject'],
  methods: {
    /**
     * Emits a closeObject event with false value
     * @emits closeObject
     */
    closeObject () {
      this.$emit('closeObject', false)
    }
  }
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
