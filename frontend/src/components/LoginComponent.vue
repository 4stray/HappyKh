<template>
 <div id="login">
   <h1>Sign up</h1>
   <input type="text" name="username" v-model="input.username" placeholder="Username" />
   <input type="password" name="password" v-model="input.password" placeholder="Password" />
   <button class="btn-login" type="button" v-on:click="login()">Login</button>
 </div>
</template>

<script>
   export default {
       name: 'LoginComponent',
       data() {
           return {
               input: {
                   username: '',
                   password: '',
               },
           };
       },
       methods: {
           login() {},
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
