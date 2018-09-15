<template>
  <form id="login" method="post" @submit.prevent="login" novalidate>
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
      axios.post('http://localhost:8000/api/users/login/', userCredentials)
        .then((response) => {
          this.$router.push('/');
        }).catch((error) => {
        this.$awn.alert("Account with such an email does not exist");
        this.userPassword='';
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
  },
};
</script>

<style scoped lang="scss">
</style>
