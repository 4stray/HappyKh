<template>
  <div class="HomeComponent">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
export default {
  name: 'HomeComponent',
  props: {
    msg: String,
  },
};
</script>

<style scoped lang="scss">

</style>

