<template>
  <div id="profile">
    <Header/>
    <ProfileComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from '@/components/Header.vue';
import ProfileComponent from '@/components/ProfileComponent.vue';

export default {
  name: 'Profile',
  components: {
    Header,
    ProfileComponent,
  },
};
</script>
