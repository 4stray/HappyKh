<template>
  <div>
    <div class="create-place-container">
      <div class="text-xs-right">
        <v-btn class="info" large
               :to="{ name: 'createPlace' }"
               name="create-place-button">
          Add Place
        </v-btn>
      </div>
    </div>
    <div>
      <v-container grid-list-xl name="place-container">
        <v-layout row wrap>
          <PlaceCollectionComponent v-for="place in allPlaces"
                                    v-bind:place="place"
                                    :key="place.id"/>
        </v-layout>
      </v-container>
    </div>
  </div>
</template>

<script>
import PlaceCollectionComponent from './PlaceCollectionComponent.vue';

export default {
  name: 'PlacesComponent',
  components: {
    PlaceCollectionComponent,
  },
  data() {
    return {
      allPlaces: [],
    };
  },
  created() {
    this.$store.getters.getPlaces.then((response) => {
      this.allPlaces = response.data;
    }).catch((error) => {
      if (error.response === undefined) {
        this.$awn.alert('A server error has occurred, try again later');
      } else {
        this.$awn.alert(error);
      }
    });
  },
};
</script>

<style scoped>
.create-place-container {
  margin: 0 auto;
  padding: 0 auto;
  width: 60%;
}
</style>

