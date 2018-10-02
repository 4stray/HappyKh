<template>
  <div class="place-body">
    <div class="place-image">
      <img v-bind:src=place.logo alt="Uploading picture has failed">
    </div>

    <div>
      <p>Name: {{ place.name }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlaceComponent',
  props: [
    'place',
  ],
};
</script>

<style scoped>
.place-body {
  width: 40%;
  border: 1px solid #CCCCCC;
  background-color: #FFFFFF;
  box-shadow: 3px 3px 2px grey;
  margin: 20px;
  display: inline-block;
}
.place-image {
  height: 60px;
}
</style>
