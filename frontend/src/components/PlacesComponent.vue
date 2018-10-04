<template>
  <div class="places-container">
      <div class="add-place-button">
        <router-link class="create-place-button" :to="{ name: 'createPlace' }">
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
        Authorization: `Token ${this.$store.getters.getToken}`,
      },
    };

    axios.get(allPlacesUrl, apiConfig).then((response) => {
      this.allPlaces = response.data
    }).error((error) => {
      console.log(error);
    });
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
  width: 200px;
  margin-left: auto;
  margin-right: 0px;
}

.create-place-button {
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  margin-top: 5px;
  background-color: #ffc107;
  color: #fff;
  border: none;
  padding: 10px 25px;
  text-transform: uppercase;
  font-family: "Liberation Sans", sans;
  border-radius: 20px;
  cursor: pointer;
}

.create-place-button:hover {
  background-color: #ffa000;
}

</style>

