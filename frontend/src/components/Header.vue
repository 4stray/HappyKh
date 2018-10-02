<template>
  <v-toolbar>
    <v-btn :to="{ name: 'home'}" flat exact>Home</v-btn>
    <v-btn v-if="isAuthenticated" :to="{ name: 'profile'}" flat exact>Profile
    </v-btn>
    <v-btn v-if="!isAuthenticated" :to="{ name: 'login'}" flat exact>Login
    </v-btn>
    <v-spacer></v-spacer>
    <v-btn
        v-if="isAuthenticated"
        v-on:click.native="signOut()"
        :to="{name: 'login'}"
        flat color="error" exact>Sign out
    </v-btn>

  </v-toolbar>
</template>

<script>
  import {mapGetters} from 'vuex';

  export default {
    name: 'Header',
    computed: {
      ...mapGetters({
        isAuthenticated: 'getAuthenticated',
      }),
    },
    methods: {
      signOut() {
        this.$cookies.remove('token');
        this.$cookies.remove('user_id');
        this.$router.push({name: 'home'});
        if (document.location.pathname === '/') {
          document.location.reload(true);
        }
      },
    },
  };
</script>
<style scoped lang="scss">
  #nav {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    height: 50px;
    /*position: fixed;*/
    /*top: 0;*/
    /*left: 0;*/
    width: 100%;

    box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.2), 0 4px 5px 0 rgba(0, 0, 0, 0.14), 0 1px 10px 0 rgba(0, 0, 0, 0.12);
    -webkit-box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.2), 0 4px 5px 0 rgba(0, 0, 0, 0.14), 0 1px 10px 0 rgba(0, 0, 0, 0.12);
    -moz-box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.2), 0 4px 5px 0 rgba(0, 0, 0, 0.14), 0 1px 10px 0 rgba(0, 0, 0, 0.12);

    display: flex;
    align-items: center;
    justify-content: flex-start;

    #left-nav {
      flex: 1 1 auto;
      display: flex;
      justify-content: flex-end;
    }

    a {
      font-weight: bold;
      font-size: 20px;
      color: #2c3e50;
      text-decoration: none;
      display: inline-block;
      padding: 0 20px;

      &.router-link-exact-active {
        color: #42b983;
      }
      &:hover {
        color: #42b983;
      }
    }

  }
</style>
