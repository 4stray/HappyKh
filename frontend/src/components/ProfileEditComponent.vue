<template>
  <v-card class="v-card pa-5 mb-5">
    <v-card-title primary-title>
      <h3 class="headline mb-0">Edit your profile:</h3>
    </v-card-title>
    <v-form @submit.prevent="save">
      <v-text-field type="text" id="first_name" label="First name"
                    v-model="userFirstName"
                    placeholder="First name"></v-text-field>
      <v-text-field type="text" id="last_name" label="Last name"
                    v-model="userLastName"
                    placeholder="Last name"></v-text-field>
      <v-text-field type="number" id="age" v-model="userAge" label="Age"
                    min="0" max="140" step="1"></v-text-field>
      <v-radio-group v-model="userGender" label="Gender">
        <v-radio label="Woman" color="primary" value="W"></v-radio>
        <v-radio label="Male" color="primary" value="M"></v-radio>
      </v-radio-group>
      <v-label for="imageInput">Choose image for download</v-label>
      <img v-bind:src=userImage id='image' alt="No profile image"
           width="300px"/>
      <input type="file"
             id="imageInput"
             class="file-upload"
             v-on:change="changeImage()"
             accept="image/*"/>
      <v-btn class="success" type="submit" block>Save</v-btn>
    </v-form>
  </v-card>
</template>

<script>
import axios from 'axios';

const UserAPI = 'http://127.0.0.1:8000/api/users/';

export default {
  name: 'ProfileEditComponent',
  components: {},
  data() {
    return {
      userFirstName: '',
      userLastName: '',
      userAge: 0,
      userGender: 'M',
      userImage: '',
      valid: true,
    };
  },
  created() {
    this.fetchUserCredentials();
  },
  methods: {
    fetchUserCredentials() {
      axios.get(
        UserAPI + this.$cookies.get('user_id'),
        {
          headers: {Authorization: `Token ${this.$cookies.get('token')}`},
        },
      ).then((response) => {
        this.userFirstName = response.data.first_name;
        this.userLastName = response.data.last_name;
        this.userAge = response.data.age;
        this.userGender = response.data.gender;
        this.userImage = response.data.profile_image;
      }).catch((error) => {
        this.$awn.warning(error.message);
      });
    },
    save() {
      if (Number.isInteger(Number(this.userAge))) {
        const userCredentials = {
          first_name: this.userFirstName,
          last_name: this.userLastName,
          age: this.userAge,
          gender: this.userGender,
          profile_image: this.userImage,
        };

        axios.patch(
          UserAPI + this.$cookies.get('user_id'), userCredentials,
          {
            headers: {Authorization: `Token ${this.$cookies.get('token')}`},
          },
        ).then((response) => {
          this.userFirstName = response.data.first_name;
          this.userLastName = response.data.last_name;
          this.userAge = response.data.age;
          this.userGender = response.data.gender;
          this.userImage = response.data.profile_image;
          this.$awn.success('Your profile was successfully updated.');
        }).catch((error) => {
          this.$awn.warning(error.message);
        });
      } else {
        this.userAge = 0;
        this.$awn.warning('Enter valid age.');
      }
    },
    changeImage() {
      const file = document.getElementById('imageInput').files[0];
      const reader = new FileReader();
      const self = this;
      reader.addEventListener('load', () => {
        self.userImage = reader.result;
      }, false);
      reader.readAsDataURL(file);
    },
  },
};
</script>

<style scoped>

</style>
