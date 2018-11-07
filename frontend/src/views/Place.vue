<template>
  <v-container grid-list-md fluid>
    <GoBackComponent/>
    <PlaceDetailComponent />
  </v-container>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import Header from '@/components/Header.vue';
import PlaceDetailComponent from '@/components/PlaceDetailComponent.vue';
import GoBackComponent from '@/components/GoBackComponent.vue';

export default {
  name: 'Profile',
  components: {
    Header,
    PlaceDetailComponent,
    GoBackComponent,
  },
};
</script>
