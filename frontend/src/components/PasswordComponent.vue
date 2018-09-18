<template>
  <div id="PasswordComponent">
    <h1>Change your password:</h1>
    <input type="password" name="password" v-model="oldPassword" placeholder="Old password"/>
    <input type="password" name="password" v-model="newPassword1" placeholder="New password"/>
    <input type="password" name="password" v-model="newPassword2" placeholder="Confirm new password"/>
    <button class="btn-save-password" type="button" v-on:click="saveNewPassword()">Save password</button>
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
        newPassword1: '',
        newPassword2: '',
      };
    },
    methods: {
      saveNewPassword() {
        const userCredentials = {
          old_password: this.oldPassword,
          new_password1: this.newPassword1,
          new_password2: this.newPassword2,
        };
        axios.patch(UserAPI + this.$cookies.get('user_id'), userCredentials)
            .then((response) => {
              if (response.data.status) {
                alert('Password successfully changed.');
              } else {
                alert(response.data.message);
              }
            }).catch((error) => {
          alert(error);
        });
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
