<template>
  <v-layout align-center justify-center row fill-height>
    <v-flex xs6>
      <v-card class="v-card pa-5 mb-5" id="PlaceEditComponent">
        <h1>Edit the place:</h1>
        <v-form id="placeForm" enctype="multipart/form-data"
                @submit.prevent="save">
          <v-text-field type="text" id="name"
                        v-model="place.name"
                        label="Place name"
          ></v-text-field>
          <v-text-field id="placeAddress" label="Place Address"
                        v-model="place.address" type="text">
          </v-text-field>
          <v-textarea id="description"
                      v-model="place.description"
                      label="Description"
          ></v-textarea>
          <div>
              <img v-if="place.logo" v-bind:src=place.logo id='logo'
                   alt="Place image"/>
              <img v-else src="../assets/default_place.png" id='default_logo'
                   alt="Default place image"/>
          </div>
          <input type="file" id="logoInput" v-on:change="changeImage()"
                 accept="image/*"/>
          <v-btn class="success mt-3" type="submit" block>Apply Changes</v-btn>
        </v-form>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios';

const BaseURL = 'http://127.0.0.1:8000/api';
export default {
  name: 'PlaceEditComponent',
  data() {
    return {
      place: {
        name: '',
        logo: '',
        description: '',
        address: '',
      },
    };4
  },
  created() {
    const placeId = parseInt(this.$route.params.placeId);

    this.$store.getters.getPlace(placeId).then(response => {
      this.place = {
        name: response.data.name,
        logo: response.data.logo,
        description: response.data.description,
        address: response.data.address,
      };
    }).catch(error => {
      this.$awn.alert('User access denied for editing the place');
      this.$router.push({name: 'home'});
    });
  },
  methods: {
    save() {
      const imageFile = document.querySelector('#logoInput');
      const formData = new FormData();
      formData.set('user', this.$cookies.get('user_id'));
      formData.set('name', this.placeName);
      formData.set('description', this.placeDescription);
      formData.append('logo', imageFile.files[0]);
      axios.post(
        `${BaseURL}/places/`, formData,
        {
          headers: {
            Authorization: `Token ${this.$cookies.get('token')}`,
            'Content-Type': 'multipart/form-data',
          },
        },
      )
        .then(() => {
          this.$awn.success('Your place was successfully created.');
          this.$router.push({ name: 'home' });
        }).catch(() => {
          this.$awn.warning(this.error.message);
        });
    },
    changeImage() {
      const file = document.getElementById('logoInput').files[0];
      const reader = new FileReader();

      const self = this;
      reader.addEventListener('load', () => {
        self.placeLogo = reader.result;
      }, false);

      reader.readAsDataURL(file);
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
