<template>
  <div class="result-box">
    <v-card color="#f0f0f0">
      <v-card-text>
        {{ result }}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'ResultBox',
  props: {
    result: {
      type: String,
      required: true
    }
  }
}
</script>
