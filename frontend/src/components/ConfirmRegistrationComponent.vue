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
    /* eslint-disable prefer-destructuring */
    const userId = this.$route.params.userId;
    const emailToken = this.$route.params.emailToken;

    axios.post(
      `http://localhost:8000/api/users/activate/${userId}/${emailToken}/`,
      {
        userId,
        emailToken,
      },
    ).then(() => {
    }).catch(() => {
    });
  },
};
</script>
