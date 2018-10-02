<template>
  <div class="places-body">
      <div class="add-place-button">
        <router-link :to="{ name: 'createPlace' }">
          Add Place
        </router-link>
      </div>

      <div>
        <PlaceComponent v-for="place in allPlaces"
                        v-bind:place="place"/>
      </div>
  </div>
</template>

<script>
import Authentication from './Authentication/auth';
import PlaceComponent from './PlaceComponent';
import axios from 'axios';

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
    const apiUrl = 'http://localhost:8000/api/places/';
    const header = {
      headers: {
        Authorization: Authentication.getAuthenticationHeader(this)
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
    ]
    // axios.get(apiUrl, {
    //   apiUrl,
    // }).then((response) => {
    //   this.allPlaces = response.data
    // }).error((error) => {
    //   console.log(error);
    //});
  }
}
</script>

<style scoped>
.places-body {
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

