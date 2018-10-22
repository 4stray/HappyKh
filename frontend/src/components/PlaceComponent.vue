<template>
  <v-flex only-xs12 sm4>
      <v-card hover class="grey lighten-4">
        <v-img :src="place.logo || require('@/assets/default_place.png')"
               height="200px">
        </v-img>

        <v-card-title primary-title>
          <h3 class="headline mb-0 text-md-center hide-overflow">{{ place.name }}</h3>
        </v-card-title>
      </v-card>
  </v-flex>
</template>

<script>
export default {
  name: 'PlaceComponent',
  props: {
    place: {
      type: Object,
      default() {
        return {
          name: '',
          logo: '',
        };
      },
    },
  },
};
</script>

<style scoped>
</style>
