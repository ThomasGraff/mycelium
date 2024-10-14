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
          <v-list-item prepend-icon="mdi-plus" title="New Chat" value="newChat"></v-list-item>
          <v-list-item prepend-icon="mdi-pen" title="Create DataContract" value="createDataContract"></v-list-item>
          <v-list-item prepend-icon="mdi-format-list-bulleted-square" title="List DataContracts" value="listDataContracts"></v-list-item>
        </v-list>
      </v-navigation-drawer>
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

.logo-mycelium {
    text-align: center;
    padding: 10%;
  }
</style>
