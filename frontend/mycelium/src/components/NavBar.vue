<template>
  <v-app-bar app color="#212121">
    <div class="navbar-content">
      <img :src="require('@/assets/logo.png')" alt="Logo" class="logo" height="40" />
      <v-toolbar-title class="title">Mycelium</v-toolbar-title>
    </div>
    <v-spacer></v-spacer>
    <v-btn icon @click="toggleMenu">
      <v-icon>mdi-menu</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  methods: {
    toggleMenu () {
      // Logique pour afficher le menu (optionnel)
    }
  }
}
</script>

<style scoped>
.navbar-content {
  display: flex; /* Utiliser flex pour aligner les éléments horizontalement */
  align-items: center; /* Aligner verticalement */
}

.logo {
  margin-right: 8px; /* Espacement entre le logo et le titre */
  margin-left: 8px;
}

.title {
  margin: 0; /* Supprime les marges par défaut */
}
</style>
