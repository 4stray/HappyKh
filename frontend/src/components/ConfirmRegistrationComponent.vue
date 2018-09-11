<template>
  <div>
    <h2>Congratulations!!!</h2>
    <h3>You've just activated your account</h3>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'ConfirmRegistrationComponent',
  components: {
  },
  created() {
    const user_id = this.$route.params.user_id;
    const user_token = this.$route.params.token;

    axios.post(`http://localhost:8000/api/users/activate/${user_id}/${user_token}/`, {
      user_id,
      user_token,
    })
      .then((response) => {
        if (Boolean(response.data.status) === false) {
          console.log(response.data.message);
        } else {
          // get token for authorisation here
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>
