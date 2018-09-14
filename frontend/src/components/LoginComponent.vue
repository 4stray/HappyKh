<template>
  <form id="login" method="post" @submit.prevent="login">
    <div class="content">
      <input type="email" name="username" v-model.trim="userEmail"
             placeholder="EMAIL"/>
      <input type="password" name="password" v-model="userPassword"
             placeholder="PASSWORD"/>
    </div>
    <input class="btn-submit" type="submit" :disabled="isDisabledButton"
           value="LOGIN"/>
  </form>
</template>

<script>
  import axios from 'axios';
  // import {isEmailValid} from "./authentication";

  export default {
    name: 'LoginComponent',
    data() {
      return {
        userEmail: '',
        userPassword: '',
      }
    },
    methods: {
      login() {
        console.log('login');
        const userCredentials = {
          user_email: this.userEmail,
          user_password: this.userPassword,
        };
        axios.post('http://localhost:8000/api/users/login/', userCredentials)
          .then((response) => {
            console.log(response.status);
            this.$router.push('/');
          }).catch((error) => {
          console.log(error);
        });
      },
      logout() {
        const authConfig = {
          headers: {
            // Write the token of a user on the place of default one
            Authorization: 'Token c177bdde5338300b34b1d5a9f7650a3cd797bc41',
          },
        };
        axios.post('http://localhost:8000/api/users/logout/', '', authConfig)
          .then((response) => {
            console.log(response.data);
          }).catch((error) => {
          console.log(error);
        });
      },
      isEmailValid() {
        const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return re.test(this.userEmail);
      },
    },
    computed: {
      /**
       * @description Checks if user filled all fields
       * @returns {boolean}
       * */
      isDisabledButton() {
        return !(this.isEmailValid() && this.userPassword);
      },
    }
  };
</script>

<style scoped lang="scss">

</style>
