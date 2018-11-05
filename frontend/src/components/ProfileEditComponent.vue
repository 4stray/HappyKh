<template>
  <v-card class="v-card pa-5 mb-5">
    <v-card-title primary-title>
      <h3 class="headline mb-0">Edit your profile</h3>
    </v-card-title>
    <v-form ref="form" v-model="valid" @submit.prevent="save"
            enctype="multipart/form-data">
      <v-text-field type="text" id="firstName" label="First name"
                    v-model="userFirstName"
                    placeholder="First name"></v-text-field>
      <v-text-field type="text" id="lastName" label="Last name"
                    v-model="userLastName"
                    placeholder="Last name"></v-text-field>
      <v-text-field type="number" id="age" v-model="userAge" label="Age"
                    min="0" max="140" step="1"
                    :rules="ageRules"></v-text-field>
      <v-radio-group v-model="userGender" label="Gender">
        <v-radio label="Woman" color="primary" value="W"></v-radio>
        <v-radio label="Man" color="primary" value="M"></v-radio>
        <v-radio label="Other" color="primary" value="O"></v-radio>
      </v-radio-group>
      <div>
        <img v-if="userImage" v-bind:src=userImage alt="No image"/>
        <img v-else id="profile_image" src="../assets/default_user.png"
             alt="No user avatar"/>
      </div>
      <input type="file"
             id="imageInput"
             v-on:change="changeImage()"
             accept="image/*"/>
      <v-btn class="success mt-3" type="submit" block>Save</v-btn>
    </v-form>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import { axiosInstanceAuth } from '../axios-config';

export default {
  name: 'ProfileEditComponent',
  computed: {
    ...mapGetters({
      userToken: 'getToken',
      userID: 'getUserID',
    }),
  },
  data() {
    return {
      userFirstName: '',
      userLastName: '',
      userAge: 1,
      userGender: 'M',
      userImage: '',
      valid: true,
      ageRules: [
        age => (age >= 1 && age <= 140) || !age || 'Invalid age value',
      ],
    };
  },
  created() {
    this.fetchFormData();
  },
  methods: {
    fetchFormData() {
      this.$store.getters.getUserData.then((response) => {
        if (response.data.first_name === 'undefined') {
          this.userFirstName = '';
        } else {
          this.userFirstName = response.data.first_name;
        }
        if (response.data.first_name === 'undefined') {
          this.userLastName = '';
        } else {
          this.userLastName = response.data.last_name;
        }
        this.userAge = response.data.age;
        this.userGender = response.data.gender;
        this.userImage = response.data.profile_image;
      }).catch((error) => {
        if (error.response === undefined) {
          this.$awn.alert('A server error has occurred, try again later');
        } else if (error.response.data.message) {
          this.$awn.warning(error.response.data.message);
        }
      });
    },
    save() {
      if (this.$refs.form.validate()) {
        const formData = new FormData();
        formData.set('first_name', this.userFirstName);
        formData.set('last_name', this.userLastName);
        formData.set('age', this.userAge);
        formData.set('gender', this.userGender);

        const imageFile = document.querySelector('#imageInput');
        formData.append('profile_image', imageFile.files[0]);

        axiosInstanceAuth.patch(
          `/api/users/${this.userID}/data`, formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          },
        ).then((response) => {
          this.userFirstName = response.data.first_name;
          this.userLastName = response.data.last_name;
          this.userAge = response.data.age;
          this.userGender = response.data.gender;
          this.userImage = response.data.profile_image;
          this.$awn.success('Your profile was successfully updated.');
        }).catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else if (error.response.data.message) {
            this.$awn.warning(error.response.data.message);
          }
        });
      } else {
        this.$awn.warning('Please correct mistakes');
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
img {
  width: 300px;
  margin: auto;
}
</style>
