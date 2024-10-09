<!-- src/components/Navbar.vue -->
<template>
  <nav class="navbar">
    <div class="logo-container">
      <img :src="logo" alt="Logo" class="logo" />
      <span class="app-name">Data Contracts</span>
    </div>
    <div class="burger" @click="toggleMenu">☰</div>
  </nav>
</template>

<script>
import logo from '@/assets/logo.png'; // Assurez-vous que le chemin du logo est correct

export default {
  data() {
    return {
      logo, // Définir le logo dans le data
    };
  },
  methods: {
    toggleMenu() {
      // Logique pour afficher le menu
      console.log('Menu toggled');
    },
  },
};
</script>

<style scoped>
.navbar {
  background-color: #42b983; /* Couleur Vue.js */
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center; /* Centrer verticalement le logo et le burger */
  padding: 10px 20px;
  position: fixed; /* Fixe la navbar en haut */
  width: 100%;
  top: 0;
  z-index: 1000; /* Assurez-vous que la navbar est au-dessus des autres éléments */
}

.logo-container {
  display: flex;
  align-items: center; /* Centrer le logo et le texte verticalement */
}

.logo {
  height: 40px; /* Ajustez la taille du logo */
  width: auto; /* Maintenir le ratio d'aspect */
  margin-right: 10px; /* Espace entre le logo et le texte */
}

.app-name {
  font-size: 24px; /* Taille du texte */
  font-weight: bold; /* Mettre le texte en gras */
}

.burger {
  cursor: pointer;
  font-size: 24px;
}
</style>
