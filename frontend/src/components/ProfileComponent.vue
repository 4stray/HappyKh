<template>
  <v-layout justify-space-around row fill-height>
    <v-flex md4 xs12>
      <img v-if="userImage" v-bind:src=userImage alt="No image" width="80%"
           id="userImage"/>
      <img v-else src="../assets/default_user.png" alt="No user avatar"/>
    </v-flex>
    <v-flex md6 xs12>
      <v-layout justify-start column fill-height>
        <v-card id="main" class="px-5 py-3">
          <v-btn v-if=enableEditingProfile :to="{name: 'settings'}"
                 fab dark absolute bottom right color="green">
            <v-icon>edit</v-icon>
          </v-btn>
          <h3 class="headline mb-2"> {{fullName}}</h3>
          <p id="userAge" v-if="userAge">{{userAge}}</p>
          <p id="userGender" class="text--secondary">{{userGender}}</p>
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
      enableEditingProfile: false,
    };
  },
  created() {
    this.fetchUserCredentials();
  },
  computed: {
    fullName() {
      if (this.userFirstName) {
        return `${this.userFirstName} ${this.userLastName}`;
      }
      return '';
    },
  },
  methods: {
    fetchUserCredentials() {
      axios.get(
        `${UserAPI + this.$route.params.id}`,
        {
          headers: { Authorization: `Token ${this.$cookies.get('token')}` },
        },
      ).then((response) => {
        this.userFirstName = response.data.first_name;
        this.userLastName = response.data.last_name;
        this.userAge = response.data.age;
        this.userGender = GENDER_CHOICES[response.data.gender];
        this.userImage = response.data.profile_image;
        this.enableEditingProfile = response.data.enable_editing_profile;
      }).catch((error) => {
        if (error.response === undefined) {
          this.$awn.alert('A server error has occurred, try again later');
        } else if (error.response.data.message) {
          this.$awn.warning(error.response.data.message);
        }
      });
    },
  },
};
</script>

<style scoped>
.material-icons {
  display: inherit;
}
</style>
