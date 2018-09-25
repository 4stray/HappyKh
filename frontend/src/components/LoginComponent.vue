<template>
  <form id="login" method="post" @submit.prevent="login" novalidate>
    <div class="content">
      <input type="email" name="userEmail" v-model.trim="userEmail"
             placeholder="EMAIL"/>
      <input type="password" name="userPassword" v-model="userPassword"
             placeholder="PASSWORD"/>
    </div>
    <input class="btn-submit" type="submit" :disabled="isDisabledButton"
           value="LOGIN"/>
  </form>
</template>

<script>

import axios from 'axios';
import Auth from './Authentication/auth'

  export default {
    name: 'LoginComponent',
    data() {
      return {
        userEmail: '',
        userPassword: '',
      };
    },
    methods: {
      login() {
        const userCredentials = {
          user_email: this.userEmail,
          user_password: this.userPassword,
        };
        Auth.authenticate(this, userCredentials, { name: 'home' });
        this.userEmail = '';
        this.userPassword = '';
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
    },
  };
</script>

<style scoped lang="scss">
</style>
