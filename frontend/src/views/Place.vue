<template>
  <div>
    <GoBackComponent/>
    <PlaceDetailComponent />
  </div>
</template>

<script>
// @ is an alias to /src
import PlaceDetailComponent from '@/components/PlaceDetailComponent.vue';
import GoBackComponent from '@/components/GoBackComponent.vue';

export default {
  name: 'Profile',
  components: {
    PlaceDetailComponent,
    GoBackComponent,
  },
};
</script>
