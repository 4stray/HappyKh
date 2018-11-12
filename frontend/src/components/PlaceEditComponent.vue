<template>
  <v-layout align-center justify-center row fill-height>
    <v-flex xs12 md6>
      <v-card class="v-card pa-5 mb-5" id="placeEditComponent">
        <v-btn v-on:click.native="deletePlace"
                 fab dark absolute top right color="red" title="Delete Place">
          <v-icon>delete</v-icon>
        </v-btn>

        <h1>Edit the place:</h1>
          <PlaceFormComponent :place="place"
                              @savePlace="updatePlace"
                              @deletePlace="deletePlace"/>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import PlaceFormComponent from '../components/PlaceFormComponent.vue';
import { axiosInstance, getPlaceData } from '../axios-requests';

export default {
  name: 'PlaceEditComponent',
  components: {
    PlaceFormComponent,
  },
  props: {
    place: '',
  },
  created() {
    const placeId = this.$route.params.placeId;
    getPlaceData(placeId).then((response) => {
      this.place = {
        name: response.data.name,
        logo: response.data.logo,
        description: response.data.description,
        address: response.data.address,
      };
    }).catch((error) => {
      this.$awn.alert('User access denied for editing the place');
      this.$router.push({
        name: 'home',
      });
    });
  },
  methods: {
    updatePlace(formData) {
      const placeId = this.$route.params.placeId;

      axiosInstance.put(
        `/api/places/${placeId}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      ).then(() => {
        this.$awn.success('Your place was successfully edited.');
      }).catch((error) => {
        if (error.message) {
          this.$awn.warning(error.message);
        } else {
          this.$awn.alert('A server error has occurred, try again later');
        }
      });
    },
    deletePlace() {
      const placeId = this.$route.params.placeId;

      axiosInstance.delete(`/api/places/${placeId}`).then(() => {
        this.$router.push({ name: 'home' });
        this.$awn.success('Your place was successfully deleted.');
      }).catch((error) => {
        if (error.message) {
          this.$awn.warning(error.message);
        } else {
          this.$awn.alert('A server error has occurred, try again later');
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
.material-icons {
  display: inherit;
}
</style>
