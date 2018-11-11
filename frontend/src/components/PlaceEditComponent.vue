<template>
  <v-layout align-center justify-center row fill-height>
    <v-flex xs12 md6>
      <v-card class="v-card pa-5 mb-5" id="PlaceEditComponent">
        <h1>Edit the place:</h1>
          <PlaceFormComponent :place="place" @savePlace="updatePlace"/>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import PlaceFormComponent from '../components/PlaceFormComponent.vue';
import { getPlaceData } from '../axios-requests';

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
      const event = formData;

      console.log(event);
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
