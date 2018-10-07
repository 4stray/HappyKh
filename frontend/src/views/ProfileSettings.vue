<template>
  <v-layout align-start justify-center row fill-height>
    <v-flex md4>
      <v-list class="mx-4 v-card">
        <v-list-tile
          v-for="tab in tabs"
          :key="tab.title"
          @click="$vuetify.goTo(tab.component, {duration: 500, offset: 0, })"
        >{{tab.title}}
        </v-list-tile>
      </v-list>
    </v-flex>
    <v-flex md8 align-content-space-around justify-space-around reverse
            fill-height>
      <ProfileEditComponent id="profile"/>
      <PasswordComponent id="password"/>
      <ChangeEmailComponent id="email"/>
    </v-flex>
  </v-layout>
</template>

<script>
// @ is an alias to /src
import PasswordComponent from '@/components/PasswordComponent.vue';
import ChangeEmailComponent from '@/components/ChangeEmailComponent.vue';
import ProfileEditComponent from '@/components/ProfileEditComponent.vue';

export default {
  name: 'ProfileSettings',
  components: {
    PasswordComponent,
    ChangeEmailComponent,
    ProfileEditComponent,
  },
  data() {
    return {
      currentTab: ProfileEditComponent,
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

</style>
