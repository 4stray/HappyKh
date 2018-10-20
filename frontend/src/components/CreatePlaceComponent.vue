<template>
  <div id="createPlaceComponent">
    <h1>Create your place:</h1>
    <form id="placeForm" enctype="multipart/form-data">
      <input type="text" id="name"
             v-model="placeName" placeholder="Place name"/>
      <textarea id="description"
                v-model="placeDescription" placeholder="Description"></textarea>
      <img v-bind:src=placeLogo id='logo' alt="No place image"/>
      <input type="file" id="logoInput" v-on:change="changeImage()" accept="image/*"/>
      <button class="btn-save" type="button" v-on:click="save()">Create Place</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

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
        }).catch(() => {
          if (this.error.message === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else {
            this.$awn.warning(this.error.message);
          }
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
  #createPlaceComponent {
    width: 500px;
    font-family: 'Liberation Sans', sans, sans-serif;
    border: 1px solid #CCCCCC;
    background-color: #FFFFFF;
    margin: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  #placeForm {
    display: block;
  }

  #createPlaceComponent input, textarea {
    font-family: 'Liberation Sans', sans, sans-serif;
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 300px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }
  #createPlaceComponent textarea{
    resize: none;
    height: 6em;
  }
  #createPlaceComponent textarea::-webkit-scrollbar {
    width: 1em;
  }

  #createPlaceComponent textarea::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  }

  #createPlaceComponent textarea::-webkit-scrollbar-thumb {
    background-color: darkgrey;
    outline: 1px solid slategrey;
  }

  #createPlaceComponent input:focus {
    outline: none;
  }

  #createPlaceComponent img {
    font-family: 'Liberation Sans', sans, sans-serif;
    font-size: 14px;
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
