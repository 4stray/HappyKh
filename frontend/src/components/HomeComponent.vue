<template>
  <div class="HomeComponent">
    <img alt="Vue logo" src="../assets/logo_M_min.png" v-if="!isAuthenticated">
    <PlacesComponent v-if="isAuthenticated"/>
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

