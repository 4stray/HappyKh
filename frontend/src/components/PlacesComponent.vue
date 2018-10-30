<template>
  <div>
    <div class="create-place-container">
      <v-text-field  placeholder="Search" v-model="searchValue"></v-text-field>
      <div class="text-xs-right">
        <v-btn class="warning" large
               :to="{ name: 'createPlace' }"
               name="create-place-button">
          Add Place
        </v-btn>
      </div>
    </div>
    <div>
      <v-container grid-list-xl name="place-container">
        <v-layout row wrap>
          <PlaceCollectionComponent v-for="place in filteredPlaces"
                          v-bind:place="place"
                          :key="place.id"/>
        </v-layout>
      </v-container>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import filter from 'lodash/filter';
import PlaceCollectionComponent from './PlaceCollectionComponent.vue';


export default {
  name: 'PlacesComponent',
  components: {
    PlaceCollectionComponent,
  },
  computed: {
    filteredPlaces() {
      return filter(this.allPlaces, item => (item.name.indexOf(this.searchValue) !== -1));
    },
  },
  data() {
    return {
      allPlaces: [],
      searchValue: '',
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
  display: flex;
}
</style>

