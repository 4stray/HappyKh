<template>
  <div id="PlaceEdit">
    <GoBackComponent/>
    <PlaceEditComponent/>
  </div>
</template>

<script>
import PlaceEditComponent from '@/components/PlaceEditComponent.vue';
import GoBackComponent from '@/components/GoBackComponent.vue';

export default {
  name: 'PlaceEdit',
  components: {
    PlaceEditComponent,
    GoBackComponent,
  },
};
</script>

<style scoped>

</style>
