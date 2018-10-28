<template>
  <div class="CreatePlace">
    <GoBackComponent/>
    <CreatePlaceComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from '../components/Header.vue';
import CreatePlaceComponent from '../components/CreatePlaceComponent.vue';
import GoBackComponent from '@/components/GoBackComponent.vue';

export default {
  name: 'CreatePlace',
  components: {
    CreatePlaceComponent,
    Header,
    GoBackComponent,
  },
};
</script>
