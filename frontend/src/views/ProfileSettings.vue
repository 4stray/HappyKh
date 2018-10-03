<template>
  <v-layout align-start justify-center row fill-height>
    <v-flex md4>
      <v-list class="mx-4">
        <v-list-tile
            v-for="tab in tabs"
            :key="tab.title"
            @click="$vuetify.goTo(tab.component, {duration: 500, offset: 0, })"
        >{{tab.title}}
        </v-list-tile>
      </v-list>
    </v-flex>
    <v-flex md8 align-content-space-around justify-space-around reverse fill-height>
      <ProfileComponent id="profile"/>
      <PasswordComponent id="password"/>
      <ChangeEmailComponent id="email"/>
    </v-flex>
  </v-layout>
</template>
<script>
// @ is an alias to /src
import PasswordComponent from '@/components/PasswordComponent.vue';
import ChangeEmailComponent from '@/components/ChangeEmailComponent.vue';
import ProfileComponent from '@/components/ProfileEditComponent.vue';

export default {
  name: 'ProfileSettings',
  components: {
    PasswordComponent,
    ChangeEmailComponent,
    ProfileComponent,
  },
  data() {
    return {
      currentTab: ProfileComponent,
      tabs: [
        {
          title: 'Change your profile',
          component: '#profile',
        },
        {
          title: 'Change password',
          component:
              '#password',
        },
        {
          title: 'Change email',
          component:
              '#email',
        },
      ],
    };
  },
};
</script>

<style lang="scss">

  #settings-body {
    display: flex;
    justify-content: space-around;
    margin-top: 50px;

    .side-menu {
      display: flex;
      flex-direction: column;
      margin: 0 50px;

      button {
        width: 100%;
        height: 50px;
        border: none;
        padding: 10px 25px;
        color: #020203;
        background-color: transparent;
        text-transform: uppercase;
        font-weight: 600;
        cursor: pointer;
        &.active {
          border-left: 2px solid #0ca086;
        }
      }
      .panel {
        box-shadow: 0 0 15px 0 rgba(0, 0, 0, 0.4);
        -webkit-box-shadow: 0 0 15px 0 rgba(0, 0, 0, 0.4);
        -moz-box-shadow: 0 0 15px 0 rgba(0, 0, 0, 0.4);
        height: 350px;
        width: 70%;
        margin: 0 auto;
        padding: 30px 40px;
      }

      /* Small devices (portrait tablets and large phones, 600px and up) */
      @media only screen and (min-width: 600px) {
        #panel {
          width: 300px;
        }
      }
    }

  }
</style>
