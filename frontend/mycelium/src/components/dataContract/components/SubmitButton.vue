<template>
    <v-btn
    @click="submitObject">
    Submit
    </v-btn>
</template>

<script>
export default {

  methods: {
    submitObject () {
      this.$emit('submitObject', true)
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
