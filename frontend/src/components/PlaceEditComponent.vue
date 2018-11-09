<template>
  <v-layout align-center justify-center row fill-height>
    <v-flex xs12 md6>
      <v-card class="v-card pa-5 mb-5" id="PlaceEditComponent">
        <h1>Edit the place:</h1>
        <v-form id="placeForm" enctype="multipart/form-data"
                @submit.prevent="save">
          <PlaceFormComponent @updatePlace="save"/>
        </v-form>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios';
import PlaceFormComponent from '../components/PlaceFormComponent.vue';

const BaseURL = 'http://127.0.0.1:8000/api';
export default {
  name: 'PlaceEditComponent',
  components: {
    PlaceFormComponent,
  },
  created() {
    const placeId = this.$route.params.placeId;

    this.$store.getters.getPlace(placeId).then((response) => {
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
    save(formData) {
      console.log(formData);
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
