<template>
  <div>
    <v-container name="menu-container">
      <v-layout justify-center row>
        <v-flex xs2 d-inline-flex>
          <v-select
              append-icon
              :items="Object.keys(orderBy)"
              v-on:change="changeOrderBy"
              outline
              class="orderSelect"
              label="Order by"
          ></v-select>
          <v-btn id="orderIcon" :ripple="false" icon flat
                 v-on:click="changeOrder">
            <v-icon medium v-if="desc">arrow_downward</v-icon>
            <v-icon medium v-else>arrow_upward</v-icon>
          </v-btn>
        </v-flex>
        <v-flex xs6>
            <v-text-field placeholder="Search" v-model="search.onFront"
                    @keypress="pressEnter"></v-text-field>
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
import PlaceCollectionComponent from './PlaceCollectionComponent.vue';
import { getPlaces } from '../axios-requests';

export default {
  name: 'PlacesComponent',
  components: {
    PlaceCollectionComponent,
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
      this.desc = (this.desc) ? '' : '-';
      this.requestPlaces();
    },
    pressEnter(event) {
      if (event.key === 'Enter') {
        this.search.toSend = this.search.onFront;
        this.search.onFront = '';
        this.page.number = 1;
        this.requestPlaces();
      }
    },
    paginate() {
      this.requestPlaces();
    },
    requestPlaces() {
      const apiConfig = {
        params: {
          orderBy: this.currentOrder,
          order: this.desc,
          s: this.search.toSend,
          p: this.page.number,
          lim: this.page.limit,
        },
      };
      getPlaces(apiConfig).then((response) => {
        this.allPlaces = response.data.places;
        this.pagesQuantity = response.data.pages;
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
  .v-input__slot {
    border-color: blue;
  }
</style>
