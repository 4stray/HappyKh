<template>
  <v-form id="placeForm" ref="placeForm" enctype="multipart/form-data"
          @submit.prevent="savePlace" v-model="valid">

    <v-text-field type="text" id="name" v-model="place.name"
                  :rules="[rules.required]"
                  label="Place name">
    </v-text-field>

    <v-text-field id="placeAddress"
                  :rules="[rules.required, rules.address(place.address)]"
                  @change="userChangeAddress(place.address)"
                  label="Place Address"
                  v-model="place.address.address" type="text">
    </v-text-field>

    <v-textarea id="description" v-model="place.description"
                label="Description">
    </v-textarea>

    <v-img id="logoImg" :src="place.logo || require('@/assets/default_place.png')"
           height="400px" width="100%" name="place-image">
    </v-img>

    <input type="file" id="logoInput" v-on:change="changeImage"
           accept="image/*"/>
    <v-btn class="success mt-3" :disabled="!valid" type="submit" block>
      Save
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
          address: {
            type: Object,
            default() {
              return {
                longitude: '',
                latitude: '',
                address: '',
              };
            },
          },
        };
      },
    },
  },
  data() {
    return {
      autocomplete: null,
      valid: false,
      rules: {
        required: value => Boolean(value) || 'This field is required',
        address: value => (value && Boolean(value.longitude && value.latitude))
              || 'Field must be filled from drop down menu',
      },
      userChangeAddress(value) {
        this.$props.place.address.longitude = 0;
        this.$props.place.address.latitude = 0;
      },
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
    savePlace() {
      if (!this.$refs.placeForm.validate()) {
        this.$refs.placeForm.reset();
        return;
      }

      const placeId = this.$route.params.placeId;
      const formData = new FormData();

      formData.set('user', this.$store.getters.getUserID);
      formData.set('name', this.place.name);
      formData.set('description', this.place.description);
      formData.set('address', JSON.stringify(this.place.address));
      formData.append('logo', document.querySelector('#logoInput').files[0]);

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
        this.place.address = {
          latitude:
            place.geometry.location.toJSON().lat.toFixed(10),
          longitude:
            place.geometry.location.toJSON().lng.toFixed(10),
          address: place.formatted_address,
        };
      } else {
        this.place.address = {};
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
