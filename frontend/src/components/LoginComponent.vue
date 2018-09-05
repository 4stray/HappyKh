<template>
 <div id="login">
   <h1>Sign up</h1>
   <input type="text" name="username" v-model="userEmail" placeholder="Email" />
   <input type="password" name="password" v-model="userPassword" placeholder="Password" />
   <button class="btn-login" type="button" v-on:click="login()">Login</button>
 </div>
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
          if (response.data.status) {
            alert(`User exists. Full name: ${response.data.full_name}`);
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
 #login {
   width: 500px;
   border: 1px solid #CCCCCC;
   background-color: #FFFFFF;
   margin: auto;
   margin-top: 130px;
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

 .btn-login {
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

 .btn-login:hover {
   background-color: #ffa000;
 }
</style>
