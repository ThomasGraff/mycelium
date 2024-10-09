<template>
  <v-app-bar app color="#212121">
    <v-toolbar-title>
      <img :src="require('@/assets/logo.png')" alt="Logo" height="40" />
      Mycelium
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon @click="toggleMenu">
      <v-icon>mdi-menu</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  methods: {
    toggleMenu() {
      // Logique pour afficher le menu (optionnel)
    },
  },
};
</script>

<style scoped>
background-color: #42b883;
</style>
