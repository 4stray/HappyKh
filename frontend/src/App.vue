<template>
  <v-app>
    <Header/>
    <v-content class="teal lighten-5">
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>
  </v-app>
</template>

<style lang="scss">
  @import '~vue-awesome-notifications/dist/styles/style.scss';

  #app {
    font-family: 'Liberation Sans', sans, sans-serif !important;
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
