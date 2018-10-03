<template>
  <div class="places-container">
      <div class="add-place-button">
        <router-link :to="{ name: 'createPlace' }">
          Add Place
        </router-link>
      </div>

      <div class="place-components-container">
        <PlaceComponent v-for="place in allPlaces"
                        v-bind:place="place"/>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import PlaceComponent from './PlaceComponent.vue';


export default {
  name: 'PlacesComponent',
  components: {
    PlaceComponent,
  },
  data() {
    return {
      allPlaces: [],
    };
  },
  created() {
    const allPlacesUrl = 'http://localhost:8000/api/places/';
    const apiConfig = {
      headers: {
        Authorization: this.$store.getters.getToken,
      },
    };

    this.allPlaces = [
      {
        name: 'First',
      },
      {
        name: 'Second',
      },
      {
        name: 'Third',
      },
      {
        name: 'Third',
      },
      {
        name: 'Third',
      },
      {
        name: 'Third',
      },
      {
        name: 'Third',
      },
    ];
    // axios.get(allPlacesUrl, {}, apiConfig).then((response) => {
    //   this.allPlaces = response.data.all_places
    // }).error((error) => {
    //   console.log(error);
    // });
  },
};
</script>

<style scoped>
.places-container {
  margin: 0 auto;
  padding: 0 auto;
  width: 60%;
}
.add-place-button {
  width: 90px;
  margin-left: auto;
  margin-right: 0px;
}
</style>

