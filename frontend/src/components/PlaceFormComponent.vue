<template>
  <v-form id="placeForm" enctype="multipart/form-data"
          @submit.prevent="savePlace">

    <v-text-field type="text" id="name" v-model="place.name"
                  label="Place name">
    </v-text-field>

    <v-text-field id="placeAddress" label="Place Address"
                  v-model="formattedAddress" type="text">
    </v-text-field>

    <v-textarea id="description" v-model="place.description"
                label="Description">
    </v-textarea>

    <v-img :src="place.logo || require('@/assets/default_place.png')"
           height="400px" width="100%" name="place-image">
    </v-img>

    <input type="file" id="logoInput" v-on:change="changeImage"
           accept="image/*"/>
    <v-btn class="success mt-3" type="submit" block>
      Apply Changes
    </v-btn>
  </v-form>
</template>

<script>
import GoogleMapsLoader from 'google-maps';

export default {
  name: 'PlaceFormComponent',
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
  data() {
    return {
      autocomplete: null,
      formattedAddress: '',
    };
  },
  watch: {
    place(newPlaceValue) {
      this.formattedAddress = newPlaceValue.address;
    },
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
    savePlace() {
      const placeId = this.$route.params.placeId;
      const imageFile = document.querySelector('#logoInput');
      const formData = new FormData();

      if (placeId) {
        formData.set('id', placeId);
      }
      formData.set('user', this.$store.getters.getUserID);
      formData.set('name', this.place.name);
      formData.set('description', this.place.description);
      formData.set('address', this.place.address);
      formData.append('logo', imageFile.files[0]);

      this.$emit('savePlace', formData);
    },
    changeImage() {
      const file = document.getElementById('logoInput').files[0];
      const reader = new FileReader();

      reader.addEventListener('load', () => {
        this.place.logo = reader.result;
      }, false);

      reader.readAsDataURL(file);
    },
    onChange() {
      const place = this.autocomplete.getPlace();
      if (Object.keys(place).length > 1) {
        this.formattedAddress = place.formatted_address;
        this.place.address = {
          latitude:
            place.geometry.location.toJSON().lat.toFixed(10),
          longitude:
            place.geometry.location.toJSON().lng.toFixed(10),
          address: place.formatted_address,
        };
        this.place.address = JSON.stringify(this.place.address);
      } else {
        this.place.address = '';
      }
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
