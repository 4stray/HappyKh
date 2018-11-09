<template>
  <v-container>
      <v-text-field type="text" id="name"
                          v-model="place.name"
                          label="Place name">
      </v-text-field>

      <v-text-field id="placeAddress" label="Place Address"
                    v-model="formatted_address" type="text">
      </v-text-field>

      <v-textarea id="description"
                  v-model="place.description"
                  label="Description">
      </v-textarea>

      <div>
          <v-img :src="place.logo || require('@/assets/default_place.png')"
                   height="400px"
                   width="100%"
                   name="place-image">
          </v-img>
      </div>

      <input type="file" id="logoInput" v-on:change="changeImage()"
             accept="image/*"/>

      <v-btn class="success mt-3" type="submit" block>Apply Changes</v-btn>
  </v-container>
</template>

<script>
import GoogleMapsLoader from 'google-maps';

export default {
  name: "PlaceFormComponent",
  props: {
    placeProperty: {
      type: Object,
      default() {
        return {
          id: 0,
          name: 'lalala',
          logo: '',
          description: '',
          address: '',
        };
      },
    },
  },
  data() {
    return {
      place: {
        name: 'place data',
        logo: '',
        description: '',
        address: '',
      },
      formatted_address: '',
      autocomplete: null,
    };
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

    },
    changeImage() {
      const file = document.getElementById('logoInput').files[0];
      const reader = new FileReader();

      const self = this;
      reader.addEventListener('load', () => {
        self.place.image = reader.result;
      }, false);

      reader.readAsDataURL(file);
    },
    onChange() {
      const place = this.autocomplete.getPlace();
      if (Object.keys(place).length > 1) {
        this.formatted_address = place.formatted_address;
        this.place.address = {
          latitude:
            place.geometry.location.toJSON().lat.toFixed(10),
          longitude:
            place.geometry.location.toJSON().lng.toFixed(10),
          address: place.formatted_address,
        };
        this.place.address = JSON.stringify(this.place.address);
      } else { this.place.address = ''; }
    },
    test(placeValue) {
      this.$data.place = placeValue;
    },
  },
}
</script>

<style scoped>
img {
  width: 300px;
  margin: auto;
}
</style>
