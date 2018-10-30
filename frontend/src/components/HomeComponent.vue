<template>
  <div class="HomeComponent">
    <img alt="Vue logo" src="../assets/logo_M_min.png">
    <v-reponsive>
      <v-container fill-height>
        <v-layout align-center>
          <v-flex>
            <h3 class="display-2 mb-3">{{msg}}</h3>

            <span class="subheading">
              In order to join the HappyKh and get access to
              its full function set you have to sign up first
            </span>

            <v-divider class="my-3"></v-divider>

            <v-btn class="mx-0" color="info" large :to="{name: 'login'}">
              Sign Up
            </v-btn>
          </v-flex>
        </v-layout>
      </v-container>
  </v-reponsive>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import PlacesComponent from './PlacesComponent.vue';


export default {
  name: 'HomeComponent',
  components: {
    PlacesComponent,
  },
  props: {
    msg: String,
  },
  computed: {
    ...mapGetters({
      isAuthenticated: 'getAuthenticated',
    }),
  },
};
</script>

<style scoped lang="scss">

</style>

