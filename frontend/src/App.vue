<template>
  <v-app>
    <Header/>
    <v-content>
      <v-container fluid class="teal lighten-5">
        <router-view></router-view>
      </v-container>
    </v-content>
    <v-footer app></v-footer>
  </v-app>
</template>

<style lang="scss">
  @import '~vue-awesome-notifications/dist/styles/style.scss';

  #app {
    font-family: 'Liberation Sans', sans, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    width: 100%;

  }

</style>
<script>
import Header from '@/components/Header.vue';

export default {
  components: {
    Header,
  },
};
</script>
