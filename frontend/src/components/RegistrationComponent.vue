<template>
  <form id="register" action="">
    <input type="email" placeholder="EMAIL" />
    <input type="password" placeholder="PASSWORD" />
    <input type="password" placeholder="CONFIRM PASSWORD" />
    <button id="sign-up" class="btn-registration" type="submit" >SIGN UP</button>
   </form>
</template>

<script>
    export default {
        name: "RegistrationComponent"
    }
</script>

<style scoped>

    input {
        width: 100%;
        border: none;
        border-bottom: 1px solid #ff80ab;
        background-color: transparent;
        font-size: 14px;
        outline: none;
        margin: 15px 0;
    }

    .btn-registration {
        width: 100%;
        color: #fff;
        border: none;
        padding: 10px 25px;
        margin: 5px 0;
        text-transform: uppercase;
        font-weight: 600;
        font-family: 'Liberation Sans', sans;
        cursor: pointer;
    }

    #sign-up {
        background-color: #ffc107;
    }

    #btn-facebook {
        background-color: #1565c0;
    }

    #sign-up:hover {
        background-color: #ffccbc;
    }
    
    #btn-facebook:hover {
        background-color: #40c4ff;
    }

    input:focus {
        border-bottom: 1px solid #b71c1c;
    }



</style>
