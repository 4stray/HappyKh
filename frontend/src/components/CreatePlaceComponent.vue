<template>
  <div id="createPlaceComponent">
    <h1>Create your place:</h1>
    <input type="text" id="name"
           v-model="placeName" placeholder="Place name"/>
    <input type="file" id="logoInput" v-on:change="changeImage()" accept="image/*"/>
    <input type="text" id="description"
           v-model="placeDescription" placeholder="Description"/>
    <img v-bind:src=placeLogo id='image' alt="No place image"/>
    Creator: <a :href="BaseURL + '/users/' + creatorId">{{creatorName}}</a>
    <button class="btn-save" type="button" v-on:click="save()">Save changes</button>
  </div>
</template>

<script>
import axios from 'axios';
import router from '../router';
import Authentication from '../components/Authentication/auth';

const BaseURL = 'http://127.0.0.1:8000/api';
export default {
  name: 'createPlaceComponent',
  data() {
    return {
      placeName: '',
      placeLogo: '',
      placeDescription: '',
      creatorName: '',
      creatorId: '',
    };
  },
  created() {
    this.getCreatorName();
  },
  methods: {
    getCreatorName() {
      axios.get(
        `${BaseURL}/users/${this.$cookies.get('user_id')}`,
        {
          headers: { Authorization: Authentication.getAuthenticationHeader(this) },
        },
      )
        .then((response) => {
          if (response.data.first_name && response.data.last_name) { this.creatorName = `${response.data.first_name} ${response.data.last_name}`; } else { this.creatorName = response.data.email; }
        }).catch(() => {
          Authentication.signout(this);
          this.$awn.warning(this.error.message);
        });
    },
    save() {
      const placeInfo = {
        name: this.placeName,
        description: this.placeDescription,
        logo: this.placeLogo,
      };
      axios.post(
        `${BaseURL}/places/`, placeInfo,
        {
          headers: { Authorization: Authentication.getAuthenticationHeader(this) },
        },
      )
        .then(() => {
          this.$awn.success('Your place was successfully created.');
          router.push({ name: 'home' }); // TODO Change redirect location
        }).catch(() => {
          Authentication.signout(this);
          this.$awn.warning(this.error.message);
        });
    },
  },
};
</script>

<style>

</style>
