<template>
    <div>
        <p id="message" v-if="response">{{ response.message }}</p>
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
            <component v-bind:is="currentTab.component" @serverResponse="showResponse"></component>
        </div>
    </div>
</template>
<script scoped>
    import LoginComponent from '../components/LoginComponent.vue';
    import RegistrationComponent from '../components/RegistrationComponent.vue';

    const tabs = [
        {
            name: 'Sign in',
            component: LoginComponent
        },
        {
            name: 'Sign up',
            component: RegistrationComponent
        },
    ];

    export default {
        name: 'Login',
        data() {
            return {
                tabs: tabs,
                currentTab: tabs[0],
                response: '',
            }
        },
        methods: {
            showResponse(serverResponse) {
                this.response = serverResponse || '';
            },
        },
        components: {
            LoginComponent,
            RegistrationComponent,
        },
    };
</script>

<style lang="scss">
  #panel {
    background-color: #ffe4c4;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.12), 0 3px 4px rgba(0, 0, 0, 0.24);
    -webkit-box-shadow: 0 3px 5px rgba(0, 0, 0, 0.12), 0 3px 4px rgba(0, 0, 0, 0.24);
    -moz-box-shadow: 0 3px 5px rgba(0, 0, 0, 0.12), 0 3px 4px rgba(0, 0, 0, 0.24);
    height: 350px;
    width: 70%;
    margin: 30px auto;
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
      border-bottom: 3px solid #999;
      color: #999;
    }

    .active {
      color: #ff8383;
      border-bottom: 3px solid #ff8383;
    }
  }

    #message {
      width: 350px;
      //background-color: #ff8383;
     // padding: 5px 10px;
     // border-bottom: 3px solid #dc143c;
      font-size: 16px;
      margin: 10px auto;
    }

</style>
