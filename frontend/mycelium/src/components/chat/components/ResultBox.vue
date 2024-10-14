<template>
  <div class="result-box" >
    <v-card color="#f0f0f0">
      <v-card-text>
        {{ result }}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    result: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
</style>
