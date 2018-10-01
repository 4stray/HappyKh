<template>
  <div id="createPlaceComponent">
    <h1>Create your place:</h1>
    <input type="text" id="name"
           v-model="placeName" placeholder="Place name"/>
    <input type="file" id="logoInput" v-on:change="changeImage()" accept="image/*"/>
    <input type="text" id="description"
           v-model="placeDescription" placeholder="Description"/>
    <img v-bind:src=userImage id='image' alt="No profile image"/>
    <button class="btn-save" type="button" v-on:click="save()">Save changes</button>
  </div>
</template>

<script>
  export default {
      name: 'createPlaceComponent',
      data(){
        return {
          placeName: '',
          placeLogo: '',
          placeDescription: '',
          creator: '',
        };
      },
      methods:{}, 
  }
</script>

<style>

</style>