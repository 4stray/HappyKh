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
      const UserAPI = 'http://127.0.0.1:8000/api/users';
      const userCredentials = {
        user_email: this.userEmail,
        user_password: this.userPassword,
      };
      axios.post(`${UserAPI}/login/`, userCredentials)
        .then((response) => {
          this.$cookies.set('token', response.data.token);
          this.$cookies.set('user_id', response.data.user_id);

          this.$store.commit('setAuthenticated', true);

          this.$router.push({ name: 'home' });
        }).catch((error) => {
          if (error.response.data.message) {
            this.$awn.warning(error.response.data.message);
          }
          this.$cookies.remove('token');
          this.$cookies.remove('user_id');
        });
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
