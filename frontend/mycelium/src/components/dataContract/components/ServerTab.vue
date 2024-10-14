<template>
        <v-card flat>
          <v-form ref="serverForm" v-model="valid">
            <v-text-field v-model="server.name" label="Name" required></v-text-field>
            <v-text-field v-model="server.type" label="Type" required></v-text-field>
            <v-text-field v-model="server.environment" label="Environment" required></v-text-field>
            <v-text-field v-model="server.location" label="Location" required></v-text-field>
            <v-text-field v-model="server.format" label="Format" required></v-text-field>
            <v-text-field v-model="server.delimiter" label="Delimiter" required></v-text-field>
            <v-text-field v-model="server.description" label="Description" required></v-text-field>
            <v-text-field v-model="server.username" label="Username" required></v-text-field>
            <v-text-field v-model="server.passwordSecretId" label="Password Secret ID" required></v-text-field>
          </v-form>
        </v-card>
  </template>

<script>
export default {
  data () {
    return {
      server: {
        name: '', // Nom du serveur
        type: '', // Type du serveur
        environment: '', // Environnement (production, développement, etc.)
        location: '', // Localisation du serveur
        format: '', // Format de données (ex: JSON, CSV)
        delimiter: '', // Délimiteur si le format est du texte
        description: '', // Description du serveur
        username: '', // Nom d'utilisateur pour l'accès au serveur
        passwordSecretId: '' // Identifiant du secret du mot de passe
      }
    }
  },
  methods: {
    updateServer () {
      this.$emit('update', { ...this.server }) // Emit the updated server back to the parent
    }
  }
}
</script>

  <style scoped>
  .v-form {
    display: flex;
    flex-direction: column;
  }
  </style>
