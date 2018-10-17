<template>
  <v-layout v-if="isEmptyProfile()" justify-space-around row fill-height>
    <v-card class="px-5 py-3 fill-height">
      <img src="../assets/default_user.png" alt="user avatar"/>
      <h3 class="headline mb-0 mb-5">
        Your profile is empty. You can edit it.
      </h3>
      <v-btn :to="{name: 'settings'}" class="justify-self-end">Edit</v-btn>
    </v-card>
  </v-layout>
  <v-layout v-else justify-space-around row fill-height>
    <v-flex md4 xs12>
      <img v-if="userImage" v-bind:src=userImage alt="No image" width="80%"
           id="userImage"/>
      <img v-else src="../assets/default_user.png" alt="No user avatar"/>
    </v-flex>
    <v-flex md6 xs12>
      <v-layout justify-start column fill-height>
        <v-card class="px-5 py-3 fill-height">
          <v-btn :to="{name: 'settings'}"
                 fab dark absolute bottom right color="green">
            <v-icon>edit</v-icon>
          </v-btn>
          <h3 class="headline mb-2"> {{fullName}}</h3>
          <v-label v-if="userAge" class="">Age</v-label>
          <p v-if="userAge">{{userAge}}</p>
          <p class="text--secondary">{{userGender}}</p>
        </v-card>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios';

const UserAPI = 'http://127.0.0.1:8000/api/users/';
const GENDER_CHOICES = { M: 'Man', W: 'Woman' };

export default {
  name: 'ProfileComponent',
  data() {
    return {
      userFirstName: '',
      userLastName: '',
      userAge: 0,
      userGender: 'M',
      userImage: '',
      isDisabled: true,
      enableText: 'Enable editing',
    };
  },
  created() {
    this.fetchUserCredentials();
  },
  computed: {
    fullName() {
      return `${this.userFirstName} ${this.userLastName}`;
    },
  },
  methods: {
    isEmptyProfile() {
      return !(this.fullName || this.userAge || this.userImage);
    },
    fetchUserCredentials() {
      axios.get(
        `${UserAPI + this.$cookies.get('user_id')}`,
        {
          headers: { Authorization: `Token ${this.$cookies.get('token')}` },
        },
      ).then((response) => {
        this.userFirstName = response.data.first_name;
        this.userLastName = response.data.last_name;
        this.userAge = response.data.age;
        this.userGender = GENDER_CHOICES[response.data.gender];
        this.userImage = response.data.profile_image;
      }).catch((error) => {
        this.$awn.warning(error.message);
      });
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
    height: 40px;
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
