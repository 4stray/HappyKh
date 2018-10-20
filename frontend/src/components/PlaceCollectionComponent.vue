<template>
  <div class="place-body" v-on:click="detail">
    <div class="place-image">
      <img v-bind:src=place.logo alt="No picture"
           class="place-image">
    </div>

    <div class="place-name">
      <p>Name: {{ place.name }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlaceCollectionComponent',
  props: {
    place: {
      type: Object,
      default() {
        return {
          name: '',
          logo: '',
          id: '',
        };
      },
    },
  },
  methods: {
    detail() {
      this.$router.push({ name: 'placeDetail', params: { id: this.place.id } });
    },
  },
};
</script>

<style scoped>
.place-body {
  width: 40%;
  height: 250px;
  border: 1px solid #CCCCCC;
  background-color: #FFFFFF;
  box-shadow: 3px 3px 2px grey;
  margin: 20px;
  display: inline-block;
}
.place-image {
  width: 100%;
  height: 200px;
}
</style>
