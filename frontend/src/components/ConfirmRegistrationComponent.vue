<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'ConfirmRegistrationComponent',
  created() {
    /* eslint-disable prefer-destructuring */
    const userId = this.$route.params.userId;
    const emailToken = this.$route.params.emailToken;

    axios.get(
      `http://localhost:8000/api/users/activate/${userId}/${emailToken}/`,
      {
        userId,
        emailToken,
      },
    ).then((response) => {
      console.log(response.status); /* eslint-disable-line no-console */
      this.$awn.success('Your account has been activated successfully');
    }).catch((error) => {
      if (error.response === undefined) {
        this.$awn.alert('A server error has occurred, try again later');
      } else {
        this.$awn.warning(error.response.data.message);
      }
    });
    this.$router.push({ name: 'login' });
  },
};
</script>
