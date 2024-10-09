<!-- src/components/DataContract.vue -->
<template>
    <div class="data-contract">
      <h2>{{ data.title }}</h2>
      <p>{{ data.content }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: ['data'],
  };
  </script>
  
  <style scoped>
  .data-contract {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 5px;
    margin-top: 20px;
    width: 80%;
  }
  </style>
  