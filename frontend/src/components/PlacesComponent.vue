<template>
  <div>
    <div class="create-place-container">
      <v-text-field placeholder="Search" v-model="searchValue" @keyup="pressEnter"></v-text-field>
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
          <PlaceCollectionComponent v-for="place in filteredPlaces"
                                    v-bind:place="place"
                                    :key="place.id"/>
        </v-layout>
      </v-container>
    </div>
    <v-pagination
      v-model="page"
      :length="10"
      color="#2c384c"
    ></v-pagination>
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
      return filter(this.allPlaces, item => (item.name
        .toLowerCase()
        .indexOf(this.searchValue) !== -1));
    },
  },
  methods: {
    pressEnter(event) {
      const allPlacesUrl = 'http://localhost:8000/api/places/';
      const apiConfig = {
        headers: {
          Authorization: `Token ${this.$store.getters.getToken}`,
        },
      };
      if (event.key === 'Enter') {
        axios.get(`${allPlacesUrl}?option=${this.searchValue}`, apiConfig)
          .then((response) => {
            this.allPlaces = response.data;
          })
          .catch((error) => {
            if (error.response === undefined) {
              this.$awn.alert('A server error has occurred, try again later');
            } else {
              this.$awn.alert(error);
            }
          });
      }
    },
  },
  data() {
    return {
      allPlaces: [],
      searchValue: '',
      page: 1,
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

