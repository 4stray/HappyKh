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
          <h3 class="headline mb-2 font-weight-bold"
              id="placeName"> {{placeName}}</h3>
          <p v-if="placeDescription" class="subheading"
             id="placeDescription">{{placeDescription}}</p>
          <p v-else class="text--secondary" id="no_description">Place has no
            description.</p>
          <v-label class="d-block" id="labelAddress">Address</v-label>
          <h3 class="subheading" id="placeAddress"> {{placeAddress}}</h3>
        </v-card>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
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
    this.fetchPlaceData();
  },
  methods: {
    fetchPlaceData() {
      this.$store.getters.getPlace(this.$route.params.id)
        .then((response) => {
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
  word-wrap: break-word;
}
</style>
