<template>
  <v-app>
    <NavBar />
    <v-main>
      <v-container>
        <v-row :class="{ 'contract-open': showDataContract }" >
          <!-- If NO datacontract -->
          <v-col :cols="showDataContract ? 6 : 12" class="search-results-column">
            <ChatColumn
            @showDataContract="showDataContract = $event"
            />
          </v-col>
          <!-- If YES datacontract -->
          <v-col v-if="showDataContract" cols="6">
            <DataContract />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavBar from './components/NavBar.vue'
import DataContract from './components/dataContract/DataContract.vue' // Import du composant DataContract
import ChatColumn from './components/chat/ChatColumn.vue' // Import du nouveau composant ChatColumn

export default {
  components: {
    NavBar,
    DataContract, // Ajout du composant DataContract
    ChatColumn // Ajout du composant ChatColumn
  },
  data () {
    return {
      showDataContract: false // Booléen pour contrôler l'affichage du Data Contract
    }
  },
  methods: {

  }
}
</script>

<style scoped>
/* Lorsque le DataContract est ouvert, décale à gauche */
.contract-open .search-results-column {
  text-align: left;
}

/* Centre le contenu quand aucun Data Contract n'est affiché */
.search-results-column {
  text-align: center;
}
</style>
