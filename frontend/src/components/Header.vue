<template>
  <div id="nav">
    <router-link :to="{ name: 'home'}">Home</router-link>
    |
    <router-link v-if="isAuthenticated" :to="{ name: 'profile'}">Profile</router-link>
    |
    <router-link v-if="!isAuthenticated" :to="{ name: 'login'}">Login</router-link>
    <router-link v-if="isAuthenticated"
                 v-on:click.native="signOut()"
                 to="{name: login}"
                 replace>Sign out</router-link>
  </div>
</template>

<script>
import store from '../store';
import { mapGetters } from 'vuex';


export default {
  name: 'Header',
  computed: {
    ...mapGetters({
      isAuthenticated: 'getAuthenticated',
    }),
  },
  methods: {
    signOut() {
      store.dispatch('signOut');
      store.commit('signOut');
      this.$router.push({ name: 'home' });
      // if (document.location.pathname === '/') {
      //   document.location.reload(true);
      // }
    },
  },
};
</script>
<style>
  #nav {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    padding: 30px;
  }

  #nav a {
    font-weight: bold;
    color: #2c3e50;
  }

  #nav a.router-link-exact-active {
    color: #42b983;
  }

  #nav p {
    display: inline;
  }
</style>
