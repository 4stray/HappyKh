<template>
  <v-toolbar fixed app>
    <v-btn :to="{ name: 'home'}" flat exact>Home</v-btn>
    <v-btn v-if="isAuthenticated"
           :to="{ name: 'profile', params: { id: userID } }"
           flat exact>Profile
    </v-btn>
    <v-btn v-if="!isAuthenticated" :to="{ name: 'login'}" flat exact>Login
    </v-btn>
    <v-spacer></v-spacer>
    <v-btn
        v-if="isAuthenticated"
        v-on:click.native="signOut()"
        flat color="error" exact>Sign out
    </v-btn>
  </v-toolbar>
</template>

<script>
import { mapGetters } from 'vuex';
import store from '../store';

export default {
  name: 'Header',
  computed: {
    ...mapGetters({
      isAuthenticated: 'getAuthenticated',
      userID: 'getUserID',
    }),
  },
  methods: {
    signOut() {
      store.dispatch('signOut').finally(() => {
        this.$awn.success('You have been signed out');
        this.$router.push({ name: 'login' });
      });
    },
  },
};
</script>
<style scoped lang="scss">

</style>
