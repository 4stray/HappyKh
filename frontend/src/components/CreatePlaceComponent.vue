<template>
  <v-layout align-center justify-center row fill-height>
    <v-flex xs6>
      <v-card class="v-card pa-5 mb-5" id="createPlaceComponent">
        <h1>Create your place:</h1>
        <v-form id="placeForm" enctype="multipart/form-data"
                @submit.prevent="save">
          <PlaceFormComponent/>
        </v-form>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios';
import GoogleMapsLoader from 'google-maps';
import PlaceFormComponent from '../components/PlaceFormComponent.vue';

const BaseURL = 'http://127.0.0.1:8000/api';
export default {
  name: 'createPlaceComponent',
  components: {
    PlaceFormComponent,
  },
  methods: {
    save() {
      const imageFile = document.querySelector('#logoInput');
      const formData = new FormData();
      formData.set('user', this.userID);
      formData.set('name', this.placeName);
      formData.set('address', this.placeAddress);
      formData.set('description', this.placeDescription);
      formData.append('logo', imageFile.files[0]);
      axios.post(
        `${BaseURL}/places/`, formData,
        {
          headers: {
            Authorization: `Token ${this.userToken}`,
            'Content-Type': 'multipart/form-data',
          },
        },
      ).then(() => {
        this.$awn.success('Your place was successfully created.');
        this.$router.push({ name: 'home' });
      }).catch(() => {
        if (this.error.message === undefined) {
          this.$awn.alert('A server error has occurred, try again later');
        } else {
          this.$awn.warning(this.error.message);
        }
      });
    },
  },
};
</script>

<style scoped>
img {
  width: 300px;
  margin: auto;
}
</style>
