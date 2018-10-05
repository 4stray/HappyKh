<template>
  <v-layout justify-space-around row fill-height>
    <v-flex md4 xs12>
      <v-img v-bind:src=userImage alt="No image" width="80%" id="userImage"
      ></v-img>
    </v-flex>
    <v-flex md6 xs12>
      <v-layout justify-start column fill-height>
        <v-card class="px-5 py-3 fill-height">
          <h3 class="headline mb-0">{{userFirstName}} {{userLastName}}</h3>
          <p>{{userAge}}</p>
          <p>{{userGender}}</p>
          <v-btn :to="{name: 'settings'}" class="justify-self-end">Edit</v-btn>
        </v-card>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'
import Authentication from '../components/Authentication/auth'

const UserAPI = 'http://127.0.0.1:8000/api/users/'
const GENDER_CHOISES = {M: 'Man', W: 'Woman'}

export default {
  name: 'Profile',
  components: {},
  data () {
    return {
      userFirstName: '',
      userLastName: '',
      userAge: 0,
      userGender: 'M',
      userImage: '',
    }
  },
  created () {
    this.fetchUserCredentials()
  },
  methods: {
    fetchUserCredentials () {
      axios.get(
        UserAPI + this.$cookies.get('user_id'),
        {
          headers: {Authorization: Authentication.getAuthenticationHeader(this)},
        },
      ).then((response) => {
        this.userFirstName = response.data.first_name
        this.userLastName = response.data.last_name
        this.userAge = response.data.age
        this.userGender = GENDER_CHOISES[response.data.gender]
        this.userImage = response.data.profile_image
      }).catch((error) => {
        Authentication.signout(this)
        this.$awn.warning(error.message)
      })
    },
  },
};
</script>
<style scoped>
  #userImage {

  }
</style>
