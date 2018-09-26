<template>
  <div>
    <Header/>
    <h1>Congratulations!</h1>
    <p>You've just activated your account</p>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'ConfirmRegistrationComponent',
  created() {
    const userId = this.$route.params.userId;
    const emailToken = this.$route.params.emailToken;

    axios.post(
      `http://localhost:8000/api/users/activate/${userId}/${emailToken}/`,
      {
        userId,
        emailToken,
      },
    ).then((response) => {
      console.log(response.status);
    }).catch((error) => {
      console.log(error);
    });
  },
};
</script>

<style scoped>
</style>
