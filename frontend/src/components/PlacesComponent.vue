<template>
  <div>
    <v-container name="menu-container">
      <v-layout justify-space-between row>
        <v-flex xs2 d-inline-flex>
          <v-select
              append-icon
              item-text="label"
              item-value="orderBy"
              v-model="currentOrder"
              :items="items"
              v-on:change="changeOrderBy"
              return-object
              box
              label="Order by"
          ></v-select>
          <v-btn id="orderIcon" :ripple="false" icon flat
                 v-on:click="changeOrder">
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
    requestPlaces() {
      const apiConfig = {
        params: {
          orderBy: this.currentOrder.orderBy,
          order: this.desc,
        },
      };
      getPlaces(apiConfig).then((response) => {
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
