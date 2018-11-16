<script>
// @ is an alias to /src
import { getConfirmation } from '../axios-requests';

export default {
  name: 'ConfirmRegistrationComponent',
  created() {
    /* eslint-disable prefer-destructuring */
    const email = this.$route.params.email;
    const emailToken = this.$route.params.emailToken;

    getConfirmation(email, emailToken).then((response) => {
      /* eslint-disable-next-line no-console */
      console.log(response.status);
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
