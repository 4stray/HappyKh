<template>
  <v-layout justify-space-around row fill-height>
    <v-flex md6 xs12>
      <v-layout justify-start column fill-height>
        <v-card id="main" class="px-5 py-3">
          <img v-if="placeLogo" v-bind:src=placeLogo alt="No image" width="80%"
               id="placeLogo"/>
          <img v-else src="../assets/default_user.png" alt="No user avatar"/>
          <h3 class="headline mb-2"> {{placeName}}</h3>
          <v-label class="">Description</v-label>
          <p v-if="placeDescription">{{placeDescription}}</p>
          <p v-else class="text--secondary">Place don't have a description.</p>
        </v-card>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios';

const PlaceAPI = 'http://127.0.0.1:8000/api/places/';

export default {
  name: 'ProfileComponent',
  data() {
    return {
      placeLogo: '',
      placeName: '',
      placeDescription: '',
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
        this.placeDescription = response.data.description;
      }).catch((error) => {
        if (error.response.data.message) {
          this.$awn.warning(error.response.data.message);
        }
      });
    },
  },
};
</script>

<style scoped>
.material-icons {
  display: inherit;
}
</style>
