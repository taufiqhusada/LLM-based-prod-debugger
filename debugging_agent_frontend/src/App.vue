<template>
  <Header></Header>
  <div class="container">
    <Chatbox></Chatbox>
  </div>
  <Footer></Footer>

</template>

<script lang="ts">
import Chatbox from '@/components/Chatbox.vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

export default {
  components: {
    Chatbox,
    Header,
    Footer
  }
  
};
</script>

<style scoped>

</style>
