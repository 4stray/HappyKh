<template>
  <div>
    <p id="message" v-if="response"
       v-bind:class="{ successResult: response.status, errorResult: !response.status  }">
      {{
      response.message
      }}</p>
    <div id="panel">
      <div class="tabs">
        <button v-bind:class="[{ active: !signUpVisible }]"
                @click="signUpVisible = false"
        >Sign in
        </button>
        <button v-bind:class="[{ active: signUpVisible }]"
                @click="signUpVisible = true"
        >Sign up
        </button>
      </div>
      <form id="login" @submit.prevent="loginUser"
            v-if="!signUpVisible" method="post">
        <div class="content">
          <input type="email" name="username" v-model.trim="userEmail"
                 placeholder="EMAIL"/>
          <input type="password" name="password" v-model="userPassword"
                 placeholder="PASSWORD"/>
        </div>
        <input class="btn-submit" type="submit" :disabled="isDisabledLogin"
               value="Login"/>
      </form>
      <form id="register" @submit.prevent="registerUser"
            v-if="signUpVisible" method="post">
        <div class="content">
          <input type="email" v-model.trim="userEmail" placeholder="EMAIL"/>
          <p v-if="errors.email" class="error">{{errors.email}}</p>
          <input id="password" type="password" v-model="userPassword"
                 placeholder="PASSWORD"/>
          <input type="password" v-model="confirmPassword"
                 placeholder="CONFIRM PASSWORD"/>
          <ul v-if="errors.password.length">
            <li v-for="(error, index) in errors.password" :key="index"
                class="error">{{ error }}
            </li>
          </ul>
        </div>
        <input class="btn-submit" type="submit"
               :disabled="isDisabledLoginRegistration"
               value="SIGN UP"/>
      </form>
    </div>
  </div>
</template>
<script>
import { login, register } from '../components/authentication';

export default {
  name: 'Login',
  data() {
    return {
      signUpVisible: false,
      response: '',
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
    loginUser() {
      login(this, this.userCredentials);
    },
    registerUser() {
      if (this.isUserDataValid()) {
        register(this, this.userCredentials);
      }
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
    /**
       * @description Checks correctness of entered user's fields
       * @returns {boolean} Result of check
       */
    isUserDataValid() {
      this.errors = {
        email: '',
        password: [],
      };
      if (!this.isEmailValid(this.userEmail)) {
        this.errors.email = '* Please enter a valid email address.';
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
      }
      return !this.errors.length;
    },
  },
  computed: {
    /**
       * @description Checks if user filled all fields
       * @returns {boolean}
       * */
    isDisabledLoginRegistration() {
      return !(this.userEmail && this.userPassword && this.confirmPassword);
    },
    /**
       * @description Checks if user filled all fields
       * @returns {boolean}
       * */
    isDisabledLogin() {
      return !(this.isEmailValid(this.userEmail) && this.userPassword);
    },
    userCredentials() {
      return {
        user_email: this.userEmail,
        user_password: this.userPassword,
      };
    },
  },
};
</script>

<style lang="scss" scoped>
  #panel {
    background-color: #f7dbb5;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.12), 0 3px 4px rgba(0, 0, 0, 0.24);
    -webkit-box-shadow: 0 3px 5px rgba(0, 0, 0, 0.12), 0 3px 4px rgba(0, 0, 0, 0.24);
    -moz-box-shadow: 0 3px 5px rgba(0, 0, 0, 0.12), 0 3px 4px rgba(0, 0, 0, 0.24);
    height: 350px;
    width: 70%;
    margin: 20px auto;
    padding: 30px 40px;
  }

  /* Small devices (portrait tablets and large phones, 600px and up) */
  @media only screen and (min-width: 600px) {
    #panel {
      width: 300px;
    }
  }

  .tabs {
    display: flex;
    padding: 0;
    margin-bottom: 15px;
    justify-content: space-evenly;

    button {
      display: block;
      list-style: none;
      padding: 10px;
      width: 50%;
      font-size: 18px;
      font-weight: 600;
      text-align: center;
      text-decoration: none;
      text-transform: uppercase;
      border: none;
      border-bottom: 3px solid #999;
      background-color: transparent;
      color: #999;
    }

    .active {
      color: #ff8383;
      border-bottom: 3px solid #ff8383;
    }
  }

  #message {
    width: 350px;
    padding: 15px 10px;
    font-size: 16px;
    margin: 0 auto;
  }

  .errorResult {
    @extend #message;
    background-color: #ffabae;
    color: #800000;
  }

  .successResult {
    @extend #message;
    background-color: #93c54b;
    color: #02570f;
  }

  #login {
    display: flex;
    flex-direction: column;
    height: 80%;
  }

  .content {
    height: 245px;
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

  .btn-submit {
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

  .btn-submit:disabled {
    background-color: #d3d3d3;
  }

  .error {
    color: #dc143c;
    font-size: 12px;
    font-family: 'Liberation Sans', sans, sans-serif;
    margin: 2px 0;
  }

  ul {
    padding: 0;
    margin: 0;
  }

  li {
    list-style: none;
  }
</style>
