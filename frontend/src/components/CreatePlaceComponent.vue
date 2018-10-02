<template>
  <div id="createPlaceComponent">
    <h1>Create your place:</h1>
    <input type="text" id="name"
           v-model="placeName" placeholder="Place name"/>
    <textarea id="description"
              v-model="placeDescription" placeholder="Description"></textarea>
    <img v-bind:src=placeLogo id='logo' alt="No place image"/>
    <input type="file" id="logoInput" v-on:change="changeImage()" accept="image/*"/>
    <button class="btn-save" type="button" v-on:click="save()">Create Place</button>
  </div>
</template>

<script>
import axios from 'axios';
import Authentication from '../components/Authentication/auth';

const BaseURL = 'http://127.0.0.1:8000/api';
export default {
  name: 'createPlaceComponent',
  data() {
    return {
      placeName: '',
      placeLogo: '',
      placeDescription: '',
    };
  },
  methods: {
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

<style>
  #createPlaceComponent {
    width: 500px;
    border: 1px solid #CCCCCC;
    background-color: #FFFFFF;
    margin: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input, textarea {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 300px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }
  textarea{
    height: 6em;
  }
  textarea::-webkit-scrollbar {
    width: 1em;
  }

  textarea::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  }

  textarea::-webkit-scrollbar-thumb {
    background-color: darkgrey;
    outline: 1px solid slategrey;
  }

  input:focus {
    outline: none;
  }

  img {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 60%;
    height: 20%;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }

  .btn-save {
  width: 40%;
  border: none;
  border-radius: 10px;
  padding: 10px 25px;
  color: #fff;
  text-transform: uppercase;
  font-weight: 600;
  font-family: 'Liberation Sans', sans, sans-serif;
  cursor: pointer;
  background-color: #0ca086;
  }
</style>
