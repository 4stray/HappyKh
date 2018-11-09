<template>
  <v-layout :class="{'row': $vuetify.breakpoint.mdAndUp,
                     'column': $vuetify.breakpoint.smAndDown}"
            justify-space-around fill-height>
    <v-flex offset-md3 md6 xs12>
      <v-layout justify-start column>
        <v-card id="main" class="px-5 py-3">
          <v-img :src="place.logo || require('@/assets/default_place.png')"
                 height="400px"
                 width="100%"
                 name="place-image">
          </v-img>
          <v-spacer></v-spacer>
          <h3 class="headline mb-2 font-weight-bold"
            id="placeName"> {{place.name}}</h3>
          <p v-if="place.description" class="subheading text-xs-justify"
            id="placeDescription">{{place.description}}</p>
          <p v-else class="text--secondary" id="no_description">Place has no description.</p>
          <v-label class="d-block" id="labelAddress">Address</v-label>
          <h3 class="subheading" id="placeAddress"> {{place.address}}</h3>

          <v-btn :to="{name: 'placeEdit', params: {placeId: place.id}}"
             fab dark absolute bottom right color="green">
            <v-icon>edit</v-icon>
          </v-btn>
        </v-card>
      </v-layout>
    </v-flex>
    <v-flex md3 xs12>
      <v-btn :class="{'v-btn--block mt-4': $vuetify.breakpoint.smAndDown}"
             color="info" class="left">
        Request access to edit
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios';

const PlaceAPI = 'http://127.0.0.1:8000/api/places/';
const alertText = 'A server error has occurred, try again later';

export default {
  name: 'ProfileComponent',
  props: {
    place: {
      type: Object,
      default() {
        return {
          id: 0,
          name: '',
          logo: '',
          description: '',
          address: '',
        };
      },
    },
  },
  created() {
    this.fetchPlaceData();
  },
  methods: {
    fetchPlaceData() {
      axios.get(
        `${PlaceAPI + this.$route.params.id}`,
        {
          headers: { Authorization: `Token ${this.$store.getters.getToken}` },
        },
      ).then((response) => {
        this.place.id = response.data.id;
        this.place.logo= response.data.logo;
        this.place.name = response.data.name;
        this.place.address= response.data.address;
        this.place.description= response.data.description;
        if (this.place.name === '') {
          this.$awn.alert(alertText);
        }
      }).catch((error) => {
        if (error.response === undefined || error.response.status !== 200) {
          this.$awn.alert(alertText);
          this.$router.go(-1);
        } else if (error.response.data.message) {
          this.$awn.warning(error.response.data.message);
        }
      });
    },
  },
};
</script>

<style scoped>
#placeDescription {
  word-wrap:break-word;
}
.material-icons {
  display: inherit;
}
</style>
