<!-- src/components/DataContractForm.vue -->
<template>
    <form @submit.prevent="submit">
      <input
        type="text"
        v-model="title"
        placeholder="Title"
        required
      />
      <textarea
        v-model="content"
        placeholder="Content"
        required
      ></textarea>
      <button type="submit">Submit</button>
    </form>
  </template>
  
  <script>
  export default {
    data() {
      return {
        title: '',
        content: '',
      };
    },
    methods: {
      submit() {
        const newDataContract = {
          title: this.title,
          content: this.content,
        };
        this.$emit('submit', newDataContract);
        this.title = '';
        this.content = '';
      },
    },
  };
  </script>
  
  <style scoped>
  form {
    display: flex;
    flex-direction: column;
    width: 80%;
    margin-top: 20px;
  }
  
  input, textarea {
    margin-bottom: 10px;
    padding: 10px;
    font-size: 16px;
  }
  
  button {
    padding: 10px;
    background-color: #42b983; /* Couleur Vue.js */
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  </style>
  