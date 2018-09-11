<template>
  <form id="login" @submit.prevent="login">
    <div id="content">
      <input type="email" name="username" v-model.trim="userEmail"
             placeholder="EMAIL"/>
      <input type="password" name="password" v-model="userPassword"
             placeholder="PASSWORD"/>
    </div>
    <input id="btn-login" type="submit" :disabled="isDisabled"
           value="Login"/>
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
  computed: {
    /**
       * @description Checks if user filled all fields
       * @returns {boolean}
       * */
    isDisabled() {
      return !(this.isEmailValid(this.userEmail) && this.userPassword);
    },
  },
  methods: {
    /**
       *  @description Send user's credentials
       */
    login() {
      const userCredentials = {
        user_email: this.userEmail,
        user_password: this.userPassword,
      };
      axios.post('http://localhost:8000/api/users/login/', userCredentials)
        .then((response) => {
          if (response.data.status) {
            this.$router.push('/');
          } else {
            this.$emit('serverResponse', response.data.message);
          }
        }).catch((error) => {
          this.$emit('serverResponse', error);
        });
    },
    /**
       * @description Checks correctness of  user's email
       * @param {string} email
       * @returns {*|boolean}
       */
    isEmailValid(email) {
      const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      return re.test(email);
    },
  },
};
</script>

<style scoped lang="scss">
  #login {
    display: flex;
    flex-direction: column;
    height: 80%;
  }

  #content {
    height: 200px;
    flex: 1 1 auto;

    input {
      background-color: transparent;
      border: none;
      border-bottom: 2px solid #ff8383;
      font-size: 16px;
      outline: none;
      margin: 15px 0;
      width: 100%;
    }

    input:focus {
      border-bottom: 2px solid #b71c1c;
    }
  }

  #btn-login {
    width: 100%;
    border: none;
    padding: 10px 25px;
    color: #fff;
    text-transform: uppercase;
    font-weight: 600;
    font-family: 'Liberation Sans', sans, sans-serif;
    cursor: pointer;
    background-color: #ff8383;
  }

  #btn-login:disabled {
    background-color: #d3d3d3;
  }
</style>
