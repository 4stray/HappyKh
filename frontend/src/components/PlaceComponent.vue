<template>
  <div class="place-body">
    <div class="place-image">
      <img v-on:src=place.logo alt="Blank">
    </div>
    <div>
      <p>Here {{ place.name }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlaceComponent',
  props: [
    'place',
  ],
}
</script>

<style scoped>
  .place-body {
    width: 25%;
    border: 1px solid #CCCCCC;
    background-color: #FFFFEE;
    box-shadow: 3px 3px 2px grey;
    margin: 0 20px;
  }
  .place-image {
    height: 60px;
  }
</style>
