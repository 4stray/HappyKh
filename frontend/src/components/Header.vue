<template>
  <div id="nav">
    <router-link :to="{ name: 'home'}">Home</router-link>
    |
      <router-link v-if="!isAuthenticated" :to="{ name: 'login'}">Login</router-link>
      <a v-if="isAuthenticated" v-on:click="signOut()">Sign out</a>
    <div v-if="isAuthenticated">
      |
      <router-link v-if="isAuthenticated" :to="{ name: 'profile'}">Profile</router-link>
    </div>
  </div>
</template>

<script>
  import Auth from '../components/Authentication/auth'

  export default {
    name: 'Header',
    data() {
      return {
        isAuthenticated: Auth.user.authenticated,
      };
    },
    methods: {
      signOut(){
        Auth.signout(this, '/login');
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
  }

  #nav {
    padding: 30px;
  }

  #nav a {
    font-weight: bold;
    color: #2c3e50;
  }

  #nav a.router-link-exact-active {
    color: #42b983;
  }
</style>
