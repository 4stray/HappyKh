<template>
  <div class="Profile">
    <Header/>
    <ProfileComponent/>
    <PasswordComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from '@/components/Header.vue';
import ProfileComponent from '@/components/ProfileComponent.vue';
import PasswordComponent from '@/components/PasswordComponent.vue';

export default {
  name: 'Profile',
  components: {
    Header,
    ProfileComponent,
    PasswordComponent,
  },
};
</script>
