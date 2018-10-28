<template>
  <div>
    <GoBackComponent/>
    <ProfileComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import ProfileComponent from '@/components/ProfileComponent.vue';
import GoBackComponent from '@/components/GoBackComponent.vue';

export default {
  name: 'Profile',
  components: {
    ProfileComponent,
    GoBackComponent,
  },
};
</script>
<style scoped>

</style>
