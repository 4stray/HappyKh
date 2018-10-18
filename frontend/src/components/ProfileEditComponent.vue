<template>
  <v-card class="v-card pa-5 mb-5">
    <v-card-title primary-title>
      <h3 class="headline mb-0">Edit your profile:</h3>
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
        <v-radio label="Male" color="primary" value="M"></v-radio>
      </v-radio-group>
      <img v-if="userImage" v-bind:src=userImage alt="No image"/>
      <img v-else id="profileImage" src="../assets/default_user.png" alt="No user avatar"/>
      <input type="file"
             id="imageInput"
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
      ageRules: [
        age => (age > 0 || age <= 140) || 'Invalid age value',
      ],
    };
  },
  created() {
    this.fetchformData();
  },
  methods: {
    fetchformData() {
      axios.get(
        UserAPI + this.$cookies.get('user_id'),
        {
          headers: { Authorization: `Token ${this.$cookies.get('token')}` },
        },
      ).then((response) => {
        this.userFirstName = response.data.firstName;
        this.userLastName = response.data.lastName;
        this.userAge = response.data.age;
        this.userGender = response.data.gender;
        this.userImage = response.data.profileImage;
      }).catch((error) => {
        this.$awn.warning(error.message);
      });
    },
    save() {
      if (this.$refs.form.validate()) {
        const formData = new FormData();
        formData.set('firstName', this.userFirstName);
        formData.set('lastName', this.userLastName);
        formData.set('age', this.userAge);
        formData.set('gender', this.userGender);

        const imageFile = document.querySelector('#imageInput');
        formData.append('profileImage', imageFile.files[0]);

        axios.patch(
          `${UserAPI + this.$cookies.get('user_id')}/data`, formData,
          {
            headers: {
              Authorization: `Token ${this.$cookies.get('token')}`,
              'Content-Type': 'multipart/form-data',
            },
          },
        ).then((response) => {
          this.userFirstName = response.data.firstName;
          this.userLastName = response.data.lastName;
          this.userAge = response.data.age;
          this.userGender = response.data.gender;
          this.userImage = response.data.profileImage;
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
img {
  width: 300px;
  margin: auto;
}

</style>
