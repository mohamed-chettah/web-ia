<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import ListBien from './components/ListBien.vue'
import Banner from './components/Banner.vue'

/***** Train call api *****/
fetch('http://localhost:5001/train-note', {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
  },
  body: ''
});
fetch('http://localhost:5001/train-year', {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
  },
  body: ''
});
fetch('http://localhost:5001/train-garage', {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
  },
  body: ''
});
/******* *******/
</script>

<template>
    <Banner />
<ListBien />
</template>

<style scoped>

</style>
