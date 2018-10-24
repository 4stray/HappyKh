<template>
  <v-layout justify-space-around row fill-height>
    <v-flex md6>
      <v-layout justify-start column>
        <v-card id="main" class="px-5 py-3">
          <v-img :src="placeLogo || require('@/assets/default_place.png')"
                 height="400px"
                 width="100%"
                 name="place-image">
        </v-img>
          <v-spacer></v-spacer>
          <v-label class="d-block" id="labelName">Name</v-label>
          <h3 class="headline mb-2" id="placeName"> {{placeName}}</h3>
          <v-label class="" id="labelDescription">Description</v-label>
          <p v-if="placeDescription" id="placeDescription">{{placeDescription}}</p>
          <p v-else class="text--secondary" id="no_description">Place has no description.</p>
          <v-label class="d-block" id="labelAddress">Address</v-label>
          <h3 class="title mb-2" id="placeAddress"> {{placeAddress}}</h3>
        </v-card>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios';

const PlaceAPI = 'http://127.0.0.1:8000/api/places/';
const alertText = 'A server error has occurred, try again later';

export default {
  name: 'ProfileComponent',
  data() {
    return {
      placeLogo: '',
      placeName: '',
      placeDescription: '',
      placeAddress: '',
    };
  },
  created() {
    this.fetchUserCredentials();
  },
  methods: {
    fetchUserCredentials() {
      axios.get(
        `${PlaceAPI + this.$route.params.id}`,
        {
          headers: { Authorization: `Token ${this.$cookies.get('token')}` },
        },
      ).then((response) => {
        this.placeLogo = response.data.logo;
        this.placeName = response.data.name;
        this.placeAddress = response.data.address;
        this.placeDescription = response.data.description;
        if (this.placeName === '') {
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
</style>
