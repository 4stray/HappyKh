<template>
  <div id="PasswordComponent">
    <h1>Change your password:</h1>
    <input type="password" name="password" v-model="oldPassword" placeholder="Old password"/>
    <input type="password" name="password" v-model="newPassword" placeholder="New password"/>
    <input type="password" name="password" v-model="confirmationPassword"
           placeholder="Confirm new password"/>
    <button class="btn-save-password" type="button"
            v-on:click="saveNewPassword()"
            >Save password</button>
  </div>
</template>

<script>
import axios from 'axios';

const UserAPI = 'http://127.0.0.1:8000/api/users/';

export default {
  name: 'PasswordComponent',
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      confirmationPassword: '',
      passwordErrors: [],
    };
  },
  methods: {
    isPasswordValid() {
      this.passwordErrors = [];
      if (this.newPassword.length < 8) {
        this.passwordErrors.push('Your password must be at least 8 characters.');
      }
      const alphaNumeric = /^[0-9a-zA-Z]+$/;
      if (!this.newPassword.match(alphaNumeric)) {
        this.passwordErrors.push('Your password must contain only numbers and alphabetical characters.');
      }
      if (this.newPassword !== this.confirmationPassword) {
        this.passwordErrors.push("Your passwords don't match, please try again.");
      }
      if (this.newPassword !== this.confirmationPassword) {
        this.passwordErrors.push('Confirmation password is incorrect');
      }
      return this.passwordErrors.length < 1;
    },
    saveNewPassword() {
      if (this.isPasswordValid()) {
        const userCredentials = {
          old_password: this.oldPassword,
          new_password: this.newPassword,
        };
        axios.patch(
          `${UserAPI + this.$cookies.get('user_id')}/password/`, userCredentials,
          {
            headers: { Authorization: `Token ${this.$cookies.get('token')}` },
          },
        )
          .then((response) => {
            this.$awn.success('Password successfully changed.');
          }).catch((error) => {
            if (error.response.data.message) {
              this.$awn.warning(error.response.data.message);
            }
          });
      } else {
        this.passwordError.forEach((error) => {
          this.$awn.warning(error);
        });
      }
      this.newPassword = '';
      this.confirmationPassword = '';
      this.oldPassword = '';
    },
  },
};
</script>

<style scoped>

  #PasswordComponent {
    width: 500px;
    border: 1px solid #CCCCCC;
    background-color: #FFFFFF;
    margin: auto;
    margin-top: 30px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 300px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }

  input:focus {
    outline: none;
  }

  .btn-save-password {
    margin-top: 5px;
    background-color: #ffc107;
    color: #fff;
    border: none;
    padding: 10px 25px;
    text-transform: uppercase;
    font-weight: 600;
    font-family: "Liberation Sans", sans;
    border-radius: 20px;
    cursor: pointer;
  }

  .btn-save-password:hover {
    background-color: #ffa000;
  }
</style>
