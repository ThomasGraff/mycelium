<template>
  <v-app>
    <NavBar @requestObject="handleObjectRequest"/>
    <v-main>
      <v-container color="#2f2f2f">
        <v-row :class="{ 'object-open': isObjectVisible }">
          <!-- Si aucun objet n'est affiché -->
          <v-col :cols="isObjectVisible ? 6 : 12" class="search-results-column">
            <ChatColumn
              @requestObject="handleObjectRequest"
              @close-object="closeObject"
            />
          </v-col>

          <!-- Si un objet est affiché -->
          <v-col v-if="isObjectVisible" cols="6">
            <component
              :is="currentObjectComponent"
              @close-object="closeObject"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavBar from './components/navigation/NavBar.vue'
import DataContract from './components/dataContract/DataContract.vue' // Import du composant DataContract
import ListDataContracts from './components/listDataContracts/ListDataContracts.vue' // Import du composant ListDataContracts
import ChatColumn from './components/chat/ChatColumn.vue' // Import du composant ChatColumn

export default {
  components: {
    NavBar,
    DataContract,
    ListDataContracts,
    ChatColumn
  },
  data () {
    return {
      isObjectVisible: false, // Booléen pour contrôler l'affichage des objets
      currentObjectComponent: null // Composant à afficher
    }
  },
  methods: {
    handleObjectRequest (objectType) {
      this.isObjectVisible = true
      this.currentObjectComponent = objectType // Définit le composant à afficher
    },
    closeObject () {
      this.isObjectVisible = false
      this.currentObjectComponent = null // Réinitialise le composant affiché
    }
  }
}
</script>

<style scoped>
/* Lorsque l'objet est ouvert, déplace à gauche */
.object-open .search-results-column {
  text-align: left;
}

/* Centre le contenu quand aucun objet n'est affiché */
.search-results-column {
  text-align: center;
}
</style>
