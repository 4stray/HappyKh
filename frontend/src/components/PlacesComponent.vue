<template>
  <div>
    <div class="create-place-container">
      <v-text-field placeholder="Search" v-model="search.onFront"
                    @keypress="pressEnter"></v-text-field>
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
    <v-pagination
      v-if="pagesQuantity>1"
      v-model="page.number"
      :length="pagesQuantity"
      color="#2c384c"
      @input="paginate"
    ></v-pagination>
  </div>
</template>

<script>
import axios from 'axios';
import PlaceCollectionComponent from './PlaceCollectionComponent.vue';

const allPlacesUrl = 'http://localhost:8000/api/places/';

export default {
  name: 'PlacesComponent',
  components: {
    PlaceCollectionComponent,
  },
  methods: {
    pressEnter(event) {
      if (event.key === 'Enter') {
        this.search.toSend = this.search.onFront;
        this.search.onFront = '';
        this.page.number = 1;
        this.page.limit = 4;
        const apiConfig = {
          headers: {
            Authorization: `Token ${this.$store.getters.getToken}`,
          },
          params: {
            s: this.search.toSend,
            p: this.page.number,
            lim: this.page.limit,
          },
        };
        this.fetchRequest(apiConfig);
      }
    },
    paginate() {
      const apiConfig = {
        headers: {
          Authorization: `Token ${this.$store.getters.getToken}`,
        },
        params: {
          p: this.page.number,
          s: this.search.toSend,
          lim: this.page.limit,
        },
      };
      this.fetchRequest(apiConfig);
    },


    fetchRequest(config) {
      axios.get(allPlacesUrl, config)
        .then((response) => {
          this.allPlaces = response.data.places;
          this.pagesQuantity = response.data.pages;
        })
        .catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else {
            this.$awn.alert(error);
          }
        });
    },
  },
  data() {
    return {
      allPlaces: [],
      pagesQuantity: 1,
      search: {
        toSend: '',
        onFront: '',
      },
      page: {
        number: 1,
        limit: 15,
      },
    };
  },
  created() {
    const apiConfig = {
      headers: {
        Authorization: `Token ${this.$store.getters.getToken}`,
      },
    };
    this.fetchRequest(apiConfig);
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

