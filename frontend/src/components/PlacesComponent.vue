<template>
  <div>
    <v-container name="menu-container">
      <v-layout justify-space-between row>
        <v-flex xs2 d-inline-flex>
          <v-select
            append-icon
            :items="Object.keys(orderBy)"
            v-on:change="changeOrderBy"
            box
            label="Order by"
          ></v-select>
          <v-btn id="orderIcon" :ripple="false" icon flat v-on:click="changeOrder">
            <v-icon medium v-if="desc">arrow_downward</v-icon>
            <v-icon medium v-else>arrow_upward</v-icon>
          </v-btn>
        </v-flex>
        <v-flex xs2>
          <v-btn class="info" large
                   :to="{ name: 'createPlace' }"
                   name="create-place-button">
              Add Place
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
    <v-container grid-list-xl name="place-container">
        <v-layout row wrap>
          <PlaceCollectionComponent v-for="place in allPlaces"
                          v-bind:place="place"
                          :key="place.id"/>
        </v-layout>
      </v-container>
  </div>
</template>

<script>
import axios from 'axios';
import PlaceCollectionComponent from './PlaceCollectionComponent.vue';


export default {
  name: 'PlacesComponent',
  components: {
    PlaceCollectionComponent,
  },
  data() {
    return {
      allPlaces: [],
      orderBy: {
        Name: 'name',
        Date: 'created',
      },
      currentOrder: 'name',
      desc: '',
    };
  },
  created() {
    this.requestPlaces();
  },
  methods: {
    changeOrderBy(key) {
      this.currentOrder = this.orderBy[key];
      this.requestPlaces();
    },
    changeOrder() {
      if (this.desc) { this.desc = ''; } else { this.desc = '-'; }
      this.requestPlaces();
    },
    requestPlaces() {
      const allPlacesUrl = 'http://localhost:8000/api/places/';
      const apiConfig = {
        headers: {
          Authorization: `Token ${this.$store.getters.getToken}`,
        },
        params: {
          orderBy: this.currentOrder,
          order: this.desc,
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
  },
};

</script>

<style scoped>
</style>
