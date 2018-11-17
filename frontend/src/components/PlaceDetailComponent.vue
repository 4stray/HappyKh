<template>
  <v-layout justify-space-around fill-height>
    <v-flex md6 xs12>
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

          <PlaceRatingComponent/>

          <v-btn v-if="place.is_editing_permitted"
                 :to="{name: 'placeEdit', params: {placeId: place.id}}"
                 fab dark absolute bottom right color="green">
            <v-icon>edit</v-icon>
          </v-btn>

          <v-btn v-else fab dark absolute bottom right color="red"
                 v-on:click="requestPlaceEditingPermission"
                 title="Request Access to Edit">

            <v-icon>lock_open</v-icon>
          </v-btn>
        </v-card>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import PlaceRatingComponent from '@/components/PlaceRatingComponent.vue';
import {
  axiosInstance, getPlaceData,
  getPlaceEditingPermission,
} from '../axios-requests';


export default {
  name: 'ProfileComponent',
  components: {
    PlaceRatingComponent,
  },
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
        is_editing_permitted: false,
      },
    };
  },
  created() {
    this.fetchPlaceEditingPermission();
    this.fetchPlaceData();
  },
  methods: {
    requestPlaceEditingPermission() {
      axiosInstance.post(`api/places/${this.place.id}/editing_permission_activation`)
        .then((response) => {
          this.$awn.success(
            'Place editing request was sent successfully.' +
            'Admins will get in touch with you within 30 minutes'
          );
        }).catch((error) => {
          this.$awn.alert('Request was not sent');
        });
    },
    fetchPlaceEditingPermission() {
      getPlaceEditingPermission(this.$route.params.id).then((response) => {
        this.place.is_editing_permitted =
          response.data.is_place_editing_permitted;
      }).catch((error) => {
        if (!error.response) {
          this.$awn.alert('A server error has occurred, try again later');
        } else {
          this.$awn.alert(error);
        }
      });
    },
    fetchPlaceData() {
      const alertText = 'A server error has occurred, try again later';
      getPlaceData(this.$route.params.id).then((response) => {
        this.place = {
          id: response.data.id,
          logo: response.data.logo,
          name: response.data.name,
          address: response.data.address,
          description: response.data.description,
          is_editing_permitted: this.place.is_editing_permitted,
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
