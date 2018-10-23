<template>
  <PlaceDetailComponent />
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import Header from '@/components/Header.vue';
import PlaceDetailComponent from '@/components/PlaceDetailComponent.vue';

export default {
  name: 'Profile',
  components: {
    Header,
    PlaceDetailComponent,
  },
};
</script>
