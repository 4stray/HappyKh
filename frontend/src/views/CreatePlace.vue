<template>
  <div class="CreatePlace">
    <GoBackComponent/>
    <CreatePlaceComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import GoBackComponent from '@/components/GoBackComponent.vue';
import Header from '../components/Header.vue';
import CreatePlaceComponent from '../components/CreatePlaceComponent.vue';

export default {
  name: 'CreatePlace',
  components: {
    CreatePlaceComponent,
    Header,
    GoBackComponent,
  },
};
</script>
