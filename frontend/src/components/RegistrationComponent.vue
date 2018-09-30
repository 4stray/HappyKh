<template>
  <form id="register" @submit.prevent="register" method="post"
        novalidate>
    <div class="content">
      <input id="userEmail" type="email" v-model.trim="userEmail" placeholder="EMAIL"/>
      <p v-if="errors.email" class="error">{{errors.email}}</p>
      <input id="userPassword" type="password" v-model="userPassword"
             placeholder="PASSWORD"/>
      <input id="confirmPassword" type="password" v-model="confirmPassword"
             placeholder="CONFIRM PASSWORD"/>
      <ul v-if="errors.password.length">
        <li v-for="(error, index) in errors.password" :key="index"
            class="error">{{ error }}
        </li>
      </ul>
    </div>
    <input class="btn-submit" type="submit"
           :disabled="isDisabledButton"
           value="REGISTER"/>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegistrationComponent',
  data() {
    return {
      userEmail: '',
      userPassword: '',
      confirmPassword: '',
      errors: {
        email: '',
        password: [],
      },
    };
  },
  methods: {
    isEmailValid() {
      const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      return re.test(this.userEmail);
    },
    /**
       * @description Checks correctness of entered user's fields
       * @returns {boolean} Result of check
       */
    isPasswordValid() {
      this.errors = {
        email: '',
        password: [],
      };
      if (!this.isEmailValid()) {
        this.errors.email = '* Please enter valid email address.';
      }
      if (this.userPassword.length < 8) {
        this.errors.password.push('* Your password must be at least 8 characters.');
      }
      const alphaNumeric = /^[0-9a-zA-Z]+$/;
      if (!this.userPassword.match(alphaNumeric)) {
        this.errors.password.push('* Your password must contain only numbers and alphabetical characters.');
      }
      if (this.userPassword !== this.confirmPassword) {
        this.errors.password.push("* Your passwords don't match, please try again.");
        this.userPassword = '';
        this.confirmPassword = '';
      }

      return Boolean(this.errors.email || this.errors.password.length);
    },
    register() {
      if (this.isPasswordValid()) {
        this.$awn.warning('Please correct your mistakes.');
      } else {
        const userCredentials = {
          user_email: this.userEmail,
          user_password: this.userPassword,
        };
        axios.post('http://localhost:8000/api/users/registration/', userCredentials)
          .then(() => {
            this.$awn.success('Successful registration. Please check your mailbox for confirmation email.');
            this.$router.push({ name: 'home' });
          }).catch((error) => {
            if (error.response.status === 400) {
              this.$awn.alert(error.response.data.message);
            } else if (error.response.status === 500 && error.response.data.message) {
              this.$awn.info(error.response.data.message);
            } else {
              this.$awn.warning('Server error');
            }
            if (this.$cookies) {
              this.$cookies.remove('token');
              this.$cookies.remove('user_id');
              // if the request fails, remove any possible user token if possible
            }
            this.userPassword = '';
            this.confirmPassword = '';
          });
      }
    },
  },
  computed: {
    /**
       * @description Checks if user filled all fields
       * @returns {boolean}
       * */
    isDisabledButton() {
      return !(this.userEmail && this.userPassword && this.confirmPassword);
    },
  },
};
</script>

<style scoped lang="scss">
</style>
