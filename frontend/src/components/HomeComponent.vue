<template>
  <div class="HomeComponent">
    <h1>{{ msg }}</h1>
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

