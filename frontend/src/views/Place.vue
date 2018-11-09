<template>
  <div>
    <GoBackComponent/>
    <PlaceDetailComponent />
    <PlaceRatingComponent />

  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import Header from '@/components/Header.vue';
import PlaceDetailComponent from '@/components/PlaceDetailComponent.vue';
import GoBackComponent from '@/components/GoBackComponent.vue';
import PlaceRatingComponent from '@/components/PlaceRatingComponent.vue';


export default {
  name: 'Profile',
  components: {
    Header,
    PlaceDetailComponent,
    GoBackComponent,
    PlaceRatingComponent,
  },
};
</script>
