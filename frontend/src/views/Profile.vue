<template>
  <div class="Profile">
    <Header/>
    <ProfileComponent/>
    <PasswordComponent/>
  </div>
</template>

<script>
  // @ is an alias to /src
  import ProfileComponent from '@/components/ProfileComponent.vue';
  import PasswordComponent from '@/components/PasswordComponent.vue';
  import Header from '@/components/Header.vue';

  export default {
    name: 'Profile',
    components: {
      ProfileComponent,
      PasswordComponent,
      Header,
    },
  };
</script>