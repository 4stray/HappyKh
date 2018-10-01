<template>
  <div>
    <button>Add Place</button>
    <div class="places-body">
      Lorem ipsum dolor sit amet, consectetur adipisicing elit.
      Adipisci aspernatur atque blanditiis eaque exercitationem facere
      fugiat libero modi neque officia pariatur quibusdam recusandae sequi
      totam veritatis vero, voluptatibus. Ab, quidem!
    </div>
  </div>
</template>

<script>
import Authentication from './Authentication/auth';
import axios from 'axios';

export default {
  name: 'PlacesComponent',
  created() {
    const apiUrl = 'http://localhost:8000/api/places/';
    const header = {
      headers: {
        Authorization: Authentication.getAuthenticationHeader(this)
      },
    };
    axios.get(apiUrl, {
      headers,
    }).then((response) => {
      // ??
    }).error((error) => {
      console.log(error);
    })
    // axios.get()
  }
}
</script>

<style scoped>
.places-body {
  margin: 0 auto;
  width: 60%;
}
</style>
