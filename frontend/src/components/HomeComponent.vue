<template>
  <div class="HomeComponent">
    <h1>{{ msg }}</h1>
    <PlacesComponent v-if="isAuthenticated"/>
  </div>
</template>

<script>
import PlacesComponent from './PlacesComponent';
import { mapGetters } from 'vuex';


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

