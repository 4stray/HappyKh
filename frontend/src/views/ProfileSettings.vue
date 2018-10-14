<template>
  <v-layout align-start justify-center row fill-height>
    <v-flex md4>
      <v-list class="mx-4 v-card">
        <v-list-tile
            v-for="tab in tabs"
            :key="tab.title"
            @click="currentTab = tab.component"
            :class="{ active : currentTab===tab.component}"
        >{{tab.title}}
        </v-list-tile>
      </v-list>
    </v-flex>
    <v-flex md6 align-content-space-around justify-space-around reverse
            fill-height>
      <component v-bind:is="currentTab"></component>
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
          component: ProfileEditComponent,
        },
        {
          title: 'Change password',
          component: PasswordComponent,
        },
        {
          title: 'Change email',
          component: ChangeEmailComponent,
        },
      ],
    };
  },
};
</script>

<style lang="scss">
  $primaryColor: #0ca086;

  .active {
    border-left: 3px solid $primaryColor;
  }
</style>
