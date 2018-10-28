<template>
  <v-btn v-on:click="routeBack" title="Go Back"
         flat fixed class="transparent custom-position">
    <v-icon color="blue" x-large>arrow_back</v-icon>
  </v-btn>
</template>

<script>
export default {
  name: "GoBackComponent",
  methods: {
    routeBack(event) {
      this.$router.go(-1);
    }
  },
}
</script>

<style scoped>
.custom-position {
  left: 0px;
  top: 0px;
  height: 100%;
}
</style>
