<template>
  <div id="panel">
   <ul class="ul-tabs">
     <li><router-link to="/login"  >Sign in</router-link></li>
     <li><router-link to="/registration" class="active"> Sign Up</router-link></li>
   </ul>
      <RegistrationComponent />
  </div>
</template>

<script>
import RegistrationComponent from '../components/RegistrationComponent.vue';

export default {
  name: 'Registration',
  components: {
    RegistrationComponent,
  },
};
</script>

<style scoped>

 #panel {
        display: flex;
        flex-direction: column;
        background-color: #ffe4c4;
        height: 350px;
        width: 55%;
        margin: 100px auto;
        padding: 50px 40px;
        box-shadow: 5px 5px 10px 0px rgba(0, 0, 0, 0.21);
        border-radius: 10px;
    }

    .ul-tabs {
        padding: 0;
        display: flex;
        justify-content: space-evenly;
        margin-bottom: 15px;
    }

    .ul-tabs > li {
        width: 50%;
        list-style: none;
        text-align: center;
    }

    a {
        text-decoration: none;
        text-transform: uppercase;
        font-size: 18px;
        color: #999;
        font-weight: 600;
        padding: 10px;
        display: block;
        border-bottom: 3px solid #999;
    }

    .active {
        color: #ff8383;
        border-bottom: 3px solid #ff8383;
    }

</style>
