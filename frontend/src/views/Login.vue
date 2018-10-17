<template>
  <div>
    <Header/>
    <div id="panel">
      <div v-if="currentTab !== tabs.sendEmail" class="tabs">
        <button
                v-bind:class="[{ active: currentTab === tabs.signIn }]"
                v-on:click="currentTab = tabs.signIn">
          SIGN IN
        </button>
        <button
                v-bind:class="[{ active: currentTab === tabs.signUp }]"
                v-on:click="currentTab = tabs.signUp"
                >SIGN UP</button>
      </div>
      <div v-else class="tabs">
        <button v-bind:class="[{ active: currentTab === tabs.sendEmail }]"
                v-on:click="currentTab = tabs.signIn">
          Back
        </button>
      </div>
      <component v-bind:is="currentTab.component"></component>
      <button
        v-if="currentTab===tabs.signIn"
        v-bind:class="[{ active: currentTab === tabs.sendEmail }]"
        v-on:click="currentTab = tabs.sendEmail" id="sendEmail">
        <span>Resend Confirmation Email</span>
      </button>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import LoginComponent from '../components/LoginComponent.vue';
import RegistrationComponent from '../components/RegistrationComponent.vue';
import ConfirmationEmailComponent from '../components/ConfirmationEmailComponent.vue';


const tabs = {
  signIn: {
    component:
      LoginComponent,
  },
  signUp: {
    component:
      RegistrationComponent,
  },
  sendEmail: {
    component:
      ConfirmationEmailComponent,
  },
};

export default {
  name: 'Login',
  data() {
    return {
      tabs,
      currentTab: tabs.signIn,
    };
  },
  components: {
    Header,
    LoginComponent,
    RegistrationComponent,
    ConfirmationEmailComponent,
  },
};
</script>

<style lang="scss">
  @import "../scss/login";

  #panel {
    box-shadow: 0 0 15px 0 rgba(0, 0, 0, 0.4);
    -webkit-box-shadow: 0 0 15px 0 rgba(0, 0, 0, 0.4);
    -moz-box-shadow: 0 0 15px 0 rgba(0, 0, 0, 0.4);
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

  #sendEmail {
    display: block;
    list-style: none;
    margin: 10px;
    width: 98%;
    font-size: 12px;
    font-weight: 300;
    text-align: center;
    text-decoration: none;
    border: none;
    background-color: transparent;
    color: $primaryColor;
    cursor: pointer;
  }

   #sendEmail span:hover{
     border-bottom: 1px solid $primaryColor;
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

      &.active {
        color: $primaryColor;
        border-bottom: 3px solid $primaryColor;
      }
    }
  }
</style>
