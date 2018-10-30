<template>
  <div class="home">
    <PlacesComponent v-if="isAuthenticated"/>
    <HomeComponent v-else msg="Welcome to HappyKh"/>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from '@/components/Header.vue';
import HomeComponent from '@/components/HomeComponent.vue';
import PlacesComponent from '@/components/PlacesComponent.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'home',
  components: {
    Header,
    HomeComponent,
    PlacesComponent,
  },
  computed: {
    ...mapGetters({
      isAuthenticated: 'getAuthenticated',
    }),
  },
};
</script>
