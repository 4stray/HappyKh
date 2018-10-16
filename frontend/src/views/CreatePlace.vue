<template>
  <div class="CreatePlace">
    <Header/>
    <CreatePlaceComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from '../components/Header.vue';
import CreatePlaceComponent from '../components/CreatePlaceComponent.vue';

export default {
  name: 'CreatePlace',
  components: {
    CreatePlaceComponent,
    Header,
  },
};
</script>
