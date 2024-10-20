<template>
  <v-btn @click="submitObject" color="primary" :disabled="isDisabled">
    {{ buttonText }}
  </v-btn>
</template>

<script>
export default {
  name: 'SubmitButton',
  props: {
    isDisabled: {
      type: Boolean,
      default: false
    },
    buttonText: {
      type: String,
      default: 'Submit'
    }
  },
  emits: ['submitObject'],
  methods: {
    submitObject () {
      this.$emit('submitObject', true)
    }
  }
}
</script>

<style scoped>
/* Styles for the card containing the button */
.v-card {
  margin-top: 20px;
  padding: 20px;
}

/* Styles for scrollable content */
.scrollable-card {
  max-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
