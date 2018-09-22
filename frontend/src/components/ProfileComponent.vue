<template>
  <div id="ProfileComponent">
    <h1>Your profile:</h1>
    <input type="text" :disabled="isDisabled" id="first_name"
           v-model="userFirstName" placeholder="First name"/>
    <input type="text" :disabled="isDisabled" id="last_name"
           v-model="userLastName" placeholder="Last name"/>
    <input type="number" :disabled="isDisabled" id="age" v-model="userAge" min="0" max="140" step="1"/>
    <select :disabled="isDisabled" v-model="userGender">
      <option disabled value="">Choose your gender</option>
      <option>Man</option>
      <option>Woman</option>
    </select>
    <img v-bind:src=userImage id='image' alt="No profile image"/>
    <input type="file" id="imageInput" :disabled="isDisabled" v-on:change="changeImage()" accept="image/*"/>
    <button class="btn-change" v-on:click=edit()>{{ enableText }}</button>
    <button class="btn-save" type="button" v-on:click="save()">Save changes</button>
  </div>
</template>

<script>
import axios from 'axios';
import Authentication from '../components/Authentication/auth';

const UserAPI = 'http://127.0.0.1:8000/api/users/';
const GENDER_CHOISES = { M: 'Man', W: 'Woman' };

export default {
  name: 'ProfileComponent',
  data() {
    return {
      userFirstName: '',
      userLastName: '',
      userAge: 0,
      userGender: 'Male',
      userImage: '',
      isDisabled: true,
      enableText: 'Enable editing',
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
          headers: { Authorization: Authentication.getAuthenticationHeader(this) },
        },
      )
        .then((response) => {
          this.userFirstName = response.data.first_name;
          this.userLastName = response.data.last_name;
          this.userAge = response.data.age;
          this.userGender = GENDER_CHOISES[response.data.gender];
          this.userImage = response.data.profile_image;
        }).catch((error) => {
          Authentication.signout(this);
          this.$awn.warning(this.error.message);
        });
    },
    save() {
      if (Number.isInteger(Number(this.userAge))) {
        const userCredentials = {
          first_name: this.userFirstName,
          last_name: this.userLastName,
          age: this.userAge,
          gender: this.userGender.charAt(0),
          profile_image: this.userImage,
        };

        axios.patch(
          UserAPI + this.$cookies.get('user_id'), userCredentials,
          {
            headers: { Authorization: Authentication.getAuthenticationHeader(this) },
          },
        )
          .then((response) => {
            this.isDisabled = true;
            this.enableText = 'Enable editing';
            this.userFirstName = response.data.first_name;
            this.userLastName = response.data.last_name;
            this.userAge = response.data.age;
            this.userGender = GENDER_CHOISES[response.data.gender];
            this.userImage = response.data.profile_image;
            this.$awn.success('Your profile was successfully updated.');
          }).catch((error) => {
            Authentication.signout(this);
            this.$awn.warning(this.error.message);
          });
      } else {
        this.userAge = 0;
        this.$awn.warning('Enter valid age.');
      }
    },
    edit() {
      this.isDisabled = !this.isDisabled;
      if (this.isDisabled) {
        this.enableText = 'Enable editing';
      } else {
        this.enableText = 'Disable editing';
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
  #ProfileComponent {
    width: 500px;
    border: 1px solid #CCCCCC;
    background-color: #FFFFFF;
    margin: auto;
    margin-top: 130px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 300px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }

  input:focus {
    outline: none;
  }

  img {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 300px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }

  select {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 332px;
    height: 35px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }

  .btn-change {
    margin-top: 5px;
    background-color: #ffc107;
    color: #fff;
    border: none;
    padding: 10px 25px;
    text-transform: uppercase;
    font-weight: 600;
    font-family: "Liberation Sans", sans;
    border-radius: 20px;
    cursor: pointer;
  }

  .btn-change:hover {
    background-color: #ffa000;
  }

  .btn-save {
    margin-top: 5px;
    background-color: #ffc107;
    color: #fff;
    border: none;
    padding: 10px 25px;
    text-transform: uppercase;
    font-weight: 600;
    font-family: "Liberation Sans", sans;
    border-radius: 20px;
    cursor: pointer;
  }

  .btn-save:hover {
    background-color: #ffa000;
  }
</style>
