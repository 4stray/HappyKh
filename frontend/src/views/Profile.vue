<template>
  <v-layout v-if="isEmptyProfile()" justify-space-around row fill-height>
    <v-card class="px-5 py-3 fill-height">
      <h3 class="headline mb-0 mb-5">
        Your profile is empty. You can edit it.
      </h3>
      <v-btn :to="{name: 'settings'}" class="justify-self-end">Edit</v-btn>
    </v-card>
  </v-layout>
  <v-layout v-else justify-space-around row fill-height>
    <v-flex md4 xs12>
      <v-img v-if="userImage" v-bind:src=userImage alt="No image" width="80%"
             id="userImage"
      ></v-img>
    </v-flex>
    <v-flex md6 xs12>
      <v-layout justify-start column fill-height>
        <v-card class="px-5 py-3 fill-height">
          <v-btn :to="{name: 'settings'}"
                 fab dark absolute top right color="green">
            <v-icon>edit</v-icon>
          </v-btn>
          <h3 class="headline mb-2"> {{fullName}}</h3>
          <p>{{userAge}}</p>
          <p class="text--secondary">{{userGender}}</p>
        </v-card>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

const UserAPI = 'http://127.0.0.1:8000/api/users/';
const GENDER_CHOISES = {M: 'Man', W: 'Woman'};

export default {
  name: 'Profile',
  components: {},
  data() {
    return {
      userFirstName: '',
      userLastName: '',
      userAge: 0,
      userGender: 'M',
      userImage: '',
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
      return !(!!this.fullName && !!this.userImage && !!this.userAge);
    },
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
        this.userGender = GENDER_CHOISES[response.data.gender];
        this.userImage = response.data.profile_image;
      }).catch((error) => {
        this.$awn.warning(error.message);
      });
    },
  },
};
</script>
<style scoped>

</style>
