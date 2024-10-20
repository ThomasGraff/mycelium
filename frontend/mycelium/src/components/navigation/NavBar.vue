<template>
  <v-navigation-drawer
    color="#212121"
    title="Mycelium"
    permanent
  >
    <div class="logo-mycelium">
      <img :src="require('@/assets/logo.png')" alt="Logo" class="logo" height="60" />
    </div>
    <v-list nav>
      <!-- Les éléments du menu -->
      <v-list-item
        prepend-icon="mdi-plus"
        title="New Chat (close object atm)"
        @click="selectMenu('newChat')"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-pen"
        title="Create DataContract"
        @click="selectMenu('createDataContract')"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-format-list-bulleted-square"
        title="List DataContracts"
        @click="selectMenu('listDataContracts')"
      ></v-list-item>
    </v-list>

    <!-- Affichage du contenu en fonction de la sélection -->
    <div class="menu-content">
      <component :is="selectedComponent" />
    </div>
  </v-navigation-drawer>
</template>

<script>
export default {
  data () {
    return {
      // Variable pour stocker le composant sélectionné
      selectedComponent: null
    }
  },
  methods: {
    // Méthode pour gérer la sélection du menu
    selectMenu (menuItem) {
      // En fonction de l'élément cliqué, on met à jour le composant sélectionné
      if (menuItem === 'newChat') {
        this.$emit('requestObject', 'newChat')
        console.log('newchat log')
      } else if (menuItem === 'createDataContract') {
        this.$emit('requestObject', 'DataContract')
        console.log('dataContract log')
      } else if (menuItem === 'listDataContracts') {
        this.$emit('requestObject', 'ListDataContracts')
      }
    }
  }
}
</script>

<style scoped>
.logo-mycelium {
  text-align: center;
  padding: 10%;
}
</style>
