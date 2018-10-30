<template>
  <div class="home">
    <HomeComponent msg="Welcome to HappyKh"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HomeComponent from '@/components/HomeComponent.vue';
import Header from '@/components/Header.vue';

export default {
  name: 'home',
  components: {
    Header,
    HomeComponent,
  },
};
</script>
