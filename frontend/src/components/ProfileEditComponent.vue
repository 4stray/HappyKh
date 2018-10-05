<template>
  <v-card class="v-card pa-4 mb-5">
    <v-card-title primary-title>
      <h3 class="headline mb-0">Edit your profile:</h3>
    </v-card-title>
    <v-form @submit.prevent="save">
      <v-text-field type="text" id="first_name" label="First name"
                    v-model="userFirstName" placeholder="First name"/>
      <v-text-field type="text" id="last_name" label="Last name"
                    v-model="userLastName" placeholder="Last name"/>
      <v-text-field type="number" id="age" v-model="userAge" label="Age"
                    min="0" max="140" step="1"/>
      <v-radio-group v-model="userGender" label="Gender">
        <v-radio
        label="Woman"
        color="primary"
        value="W"
        ></v-radio>
        <v-radio
        label="Male"
        color="primary"
        value="M"
        ></v-radio>
      </v-radio-group>
      <!--TODO: TypeError: Cannot read property 'src' of null (Vimg)"-->
      <v-label for="imageInput">Choose image for download</v-label>
      <v-img v-if="userAge" v-bind:src='userImage' id='image'
             alt="No profile image" max-width="50%"/>
      <input type="file"
             id="imageInput"
             class="file-upload"
             v-on:change="changeImage()"
             accept="image/*"/>

      <v-btn class="success" type="submit">Save</v-btn>
    </v-form>
  </v-card>
</template>

<script>
  import axios from 'axios'
  import Authentication from '../components/Authentication/auth'

  const UserAPI = 'http://127.0.0.1:8000/api/users/'

  export default {
    name: 'ProfileEditComponent',
    components: {},
    data () {
      return {
        userFirstName: '',
        userLastName: '',
        userAge: 0,
        userGender: 'M',
        userImage: '',
        valid: true,

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
          this.userGender = response.data.gender
          this.userImage = response.data.profile_image
        }).catch((error) => {
          Authentication.signout(this)
          this.$awn.warning(error.message)
        })
      },
      save () {
        if (Number.isInteger(Number(this.userAge))) {
          const userCredentials = {
            first_name: this.userFirstName,
            last_name: this.userLastName,
            age: this.userAge,
            gender: this.userGender,
            profile_image: this.userImage,
          }

          axios.patch(
            UserAPI + this.$cookies.get('user_id'), userCredentials,
            {
              headers: {Authorization: Authentication.getAuthenticationHeader(this)},
            },
          ).then((response) => {
            this.userFirstName = response.data.first_name
            this.userLastName = response.data.last_name
            this.userAge = response.data.age
            this.userGender = response.data.gender
            this.userImage = response.data.profile_image
            this.$awn.success('Your profile was successfully updated.')
          }).catch((error) => {
            Authentication.signout(this)
            console.log(error)
            this.$awn.warning(error.message)
          })
        } else {
          this.userAge = 0
          this.$awn.warning('Enter valid age.')
        }
      },
      changeImage () {
        const file = document.getElementById('imageInput').files[0]
        const reader = new FileReader()
        const self = this
        reader.addEventListener('load', () => {
          self.userImage = reader.result
        }, false)
        reader.readAsDataURL(file)
      },
    },
  }
</script>

<style scoped>

</style>
