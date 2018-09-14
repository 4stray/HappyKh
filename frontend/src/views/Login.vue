<template>
  <div>

    <div id="panel">
      <div class="tabs">
        <a
            v-for="tab in tabs"
            v-bind:key="tab.name"
            v-bind:class="[{ active: currentTab.name === tab.name }]"
            v-on:click="currentTab = tab"
        >{{ tab.name }}
        </a>
      </div>
      <component v-bind:is="currentTab.component"
                 @serverResponse="showMessage"></component>
    </div>
  </div>
</template>
<script>
  import LoginComponent from '../components/LoginComponent.vue';
  import RegistrationComponent from '../components/RegistrationComponent.vue';

  const tabs = [
    {
      name: 'Sign in',
      component: LoginComponent,
    },
    {
      name: 'Sign up',
      component: RegistrationComponent,
    },
  ];

  export default {
    name: 'Login',
    data() {
      return {
        tabs,
        currentTab: tabs[0],
      };
    },
    methods: {
      showMessage(serverResponse) {
        this.message = {
          text: serverResponse.message,
          type: serverResponse.status,
        };
      },
    },
    components: {
      LoginComponent,
      RegistrationComponent,
    },
  };
</script>
<style lang="scss">
  @import "../components/authentication";

  #panel {
    box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.4);
    -webkit-box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.4);
    -moz-box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.4);
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

    a {
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
</style>
