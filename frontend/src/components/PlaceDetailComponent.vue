<template>
  <v-layout :class="{'row': $vuetify.breakpoint.mdAndUp,
                     'column': $vuetify.breakpoint.smAndDown}"
            justify-space-around fill-height>
    <v-flex md3 order-md2 xs12>
      <v-btn :class="{'v-btn--block mt-4': $vuetify.breakpoint.smAndDown}"
             color="info" class="left">
        Request access to edit
      </v-btn>
    </v-flex>
    <v-flex offset-md3 md6 xs12>
      <v-layout column>
        <v-card id="main" class="px-5 py-3">
          <v-img :src="place.logo || require('@/assets/default_place.png')"
                 height="400px"
                 width="100%"
                 name="place-image"
                 id="logoImg">
          </v-img>

          <v-spacer></v-spacer>

          <h3 class="headline mb-2 font-weight-bold"
              id="placeName"> {{place.name}}</h3>
          <p v-if="place.description" class="subheading"
             id="placeDescription">{{place.description}}</p>
          <p v-else class="text--secondary"
             id="no_description">
            Place has no description.</p>

          <v-label class="d-block" id="labelAddress">Address</v-label>

          <h3 class="subheading" id="placeAddress">
            {{place.address.address}}
          </h3>

          <v-btn :to="{name: 'placeEdit', params: {placeId: place.id}}"
                 fab dark absolute top right color="green">
            <v-icon>edit</v-icon>
          </v-btn>
        </v-card>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import { getPlaceData } from '../axios-requests';

export default {
  name: 'ProfileComponent',
  data() {
    return {
      place: {
        id: 0,
        name: '',
        logo: '',
        description: '',
        address: {
          longitude: '',
          latitude: '',
          address: '',
        },
      },
    };
  },
  created() {
    this.fetchPlaceData();
  },
  methods: {
    fetchPlaceData() {
      const alertText = 'A server error has occurred, try again later';
      getPlaceData(this.$route.params.id).then((response) => {
        this.place = {
          id: response.data.id,
          logo: response.data.logo,
          name: response.data.name,
          address: response.data.address,
          description: response.data.description,
        };

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
  word-wrap: break-word;
  text-align: justify;
}
.material-icons {
  display: inherit;
}
</style>
