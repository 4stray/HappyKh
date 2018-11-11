<template>
  <v-layout align-center justify-center row fill-height>
    <v-flex xs6>
      <v-card class="v-card pa-5 mb-5" id="createPlaceComponent">
        <h1>Create your place:</h1>
          <PlaceFormComponent @savePlace="createPlace"/>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import PlaceFormComponent from '../components/PlaceFormComponent.vue';
import { axiosInstance } from '../axios-requests';

export default {
  name: 'createPlaceComponent',
  components: {
    PlaceFormComponent,
  },
  methods: {
    createPlace(formData) {
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
      }).catch((error) => {
        if (error.message === undefined) {
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
