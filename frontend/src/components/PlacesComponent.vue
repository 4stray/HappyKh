<template>
  <div>
    <v-container name="menu-container" id="menuContainer">
        <v-layout justify-center :class="{'row': $vuetify.breakpoint.mdAndUp,
                     'column': $vuetify.breakpoint.smAndDown}">
          <v-flex xs3 d-flex>
            <v-select
              append-icon
              item-text="label"
              item-value="orderBy"
              v-model="currentOrder"
              :items="items"
              v-on:change="changeOrderBy"
              return-object
              label="Order by"
            ></v-select>
            <v-btn id="orderIcon" :ripple="false"  flat
                   v-on:click="changeOrder">
              <v-icon medium v-if="desc">arrow_downward</v-icon>
              <v-icon medium v-else>arrow_upward</v-icon>
            </v-btn>
          </v-flex>
          <v-flex xs6>
            <v-text-field placeholder="Search" v-model="search.onFront"
                          @keypress="pressEnter" name="filter"></v-text-field>
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
      items: [
        { label: 'Name', orderBy: 'name' },
        { label: 'Date', orderBy: 'created' },
      ],
      currentOrder: { label: 'Name', orderBy: 'name' },
      desc: '',

    };
  },
  created() {
    this.requestPlaces();
  },
  methods: {
    changeOrderBy(object) {
      this.currentOrder = object;
      this.requestPlaces();
    },
    changeOrder() {
      this.desc = (this.desc) ? '' : '-';
      this.requestPlaces();
    },
    pressEnter(event) {
      if (event.key === 'Enter') {
        if (this.search.toSend !== this.search.onFront) {
          this.search.toSend = this.search.onFront;
          this.page.number = 1;
          this.requestPlaces();
        }
        this.search.onFront = '';
      }
    },
    requestPlaces() {
      const apiConfig = {
        params: {
          orderBy: this.currentOrder.orderBy,
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
  watch: {
    'page.number': function pagination() {
      this.requestPlaces();
    },
  },
};

</script>

<style scoped>
  #orderIcon{
    height: 65%;
  }
  #menuContainer{
    border: lightslategrey 2px groove;
    border-radius: 1em;
    background-color: #f6f8fc;
    box-shadow: blue;
  }
</style>
