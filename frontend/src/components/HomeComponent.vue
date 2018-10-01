<template>
  <div>
    <div class="HomeComponent">
      <h1>{{ msg }}</h1>
    </div>
    <PlacesComponent v-if="isAuthenticated"/>
  </div>
</template>

<script>
import PlacesComponent from "./PlacesComponent";
import { mapGetters } from 'vuex';
import store from '../store';


export default {
  name: 'HomeComponent',
  components: {
    PlacesComponent
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
  h3 {
    margin: 40px 0 0;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>

