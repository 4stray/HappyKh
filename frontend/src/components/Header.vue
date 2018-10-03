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
      this.$cookies.remove('token');
      this.$cookies.remove('user_id');
      this.$router.push({ name: 'home' });
      if (document.location.pathname === '/') {
        document.location.reload(true);
      }
    },
  },
};
</script>
<style scoped lang="scss">

</style>
