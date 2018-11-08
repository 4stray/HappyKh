<template>
  <v-layout align-center justify-center row fill-height>
    <v-flex xs6>
      <v-card class="v-card pa-5 mb-5" id="createPlaceComponent">
        <h1>Create your place:</h1>
        <v-form id="placeForm" enctype="multipart/form-data"
                @submit.prevent="save">
          <v-text-field type="text" id="name"
                        v-model="placeName"
                        label="Place name"
          ></v-text-field>
          <v-text-field id="placeAddress" label="Place Address"
                        v-model="formatted_address" type="text">
          </v-text-field>
          <v-textarea id="description"
                      v-model="placeDescription"
                      label="Description"
          ></v-textarea>
          <div>
              <img v-if="placeLogo" v-bind:src=placeLogo id='logo'
                   alt="Place image"/>
              <img v-else src="../assets/default_place.png" id='default_logo'
                   alt="Default place image"/>
          </div>
          <input type="file" id="logoInput" v-on:change="changeImage()"
                 accept="image/*"/>
          <v-btn class="success mt-3" type="submit" block>Create Place
          </v-btn>
        </v-form>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import GoogleMapsLoader from 'google-maps';
import { mapGetters } from 'vuex';
import { axiosInstance } from '../axios-requests';


export default {
  name: 'createPlaceComponent',
  data() {
    return {
      placeName: '',
      placeAddress: '',
      formatted_address: '',
      placeLogo: '',
      placeDescription: '',
      autocomplete: null,
    };
  },
  computed: {
    isDisabledButton() {
      return !(this.placeName && this.placeAddress);
    },
    ...mapGetters({
      userToken: 'getToken',
      userID: 'getUserID',
    }),
  },
  mounted() {
    GoogleMapsLoader.KEY = process.env.VUE_APP_GOOGLE_API;
    GoogleMapsLoader.VERSION = '3.33';
    GoogleMapsLoader.LIBRARIES = ['places'];
    GoogleMapsLoader.LANGUAGE = 'en';
    GoogleMapsLoader.REGION = 'UA';
    GoogleMapsLoader.load((google) => {
      this.autocomplete = new google.maps.places.Autocomplete(
        (document.getElementById('placeAddress')),
        { types: ['address'], strictBounds: true },
      );
      document.getElementById('placeAddress').placeholder = '';
      const geolocation = {
        lat: 50,
        lng: 36,
      };
      const circle = new google.maps.Circle({
        center: geolocation,
        radius: 20000,
      });
      this.autocomplete.setBounds(circle.getBounds());
      this.autocomplete.addListener('place_changed', this.onChange);
    });
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
      axiosInstance.post(
        '/api/places/', formData,
        {
          headers: {
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
    changeImage() {
      const file = document.getElementById('logoInput').files[0];
      const reader = new FileReader();

      const self = this;
      reader.addEventListener('load', () => {
        self.placeLogo = reader.result;
      }, false);

      reader.readAsDataURL(file);
    },
    onChange() {
      const place = this.autocomplete.getPlace();
      if (Object.keys(place).length > 1) {
        this.formatted_address = place.formatted_address;
        this.placeAddress = {
          latitude:
            place.geometry.location.toJSON().lat.toFixed(10),
          longitude:
            place.geometry.location.toJSON().lng.toFixed(10),
          address: place.formatted_address,
        };
        this.placeAddress = JSON.stringify(this.placeAddress);
      } else { this.placeAddress = ''; }
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
