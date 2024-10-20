<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
:root {
  --scrollbar-color: #212121;
}

body {
  overflow: hidden;
}

/* Global scrollbar styles */
* {
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-color) transparent;
}

/* WebKit browsers (Chrome, Safari, etc.) */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: var(--scrollbar-color);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

::-webkit-scrollbar-button {
  display: none;
}
</style>
